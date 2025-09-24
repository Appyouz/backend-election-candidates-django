from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class UserSerializer(serializers.ModelSerializer):
    """User model serializer with role display"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'role_display', 'date_joined',
            'is_active', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'role_display']
        
    def to_representation(self, instance):
        """Override to include role display name in response"""
        representation = super().to_representation(instance)
        representation['role_display'] = instance.get_role_display()
        return representation

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer that includes user role in JWT payload"""
    
    @classmethod
    def get_token(cls, user):
        """Add custom claims to token"""
        token = super().get_token(user)
        
        token['role'] = user.get_role_display()  
        token['role_id'] = user.role  
        token['email'] = user.email
        token['username'] = user.username
        token['user_id'] = user.id
        
        return token
    
    def validate(self, attrs):
        """Override validate to include role in response"""
        data = super().validate(attrs)
        
        data['role'] = self.user.get_role_display()
        data['role_id'] = self.user.role
        data['user_id'] = self.user.id
        
        return {
            'access': data['access'],
            'refresh': data['refresh'],
            'role': data['role'],
            'role_id': data['role_id'],
            'user_id': data['user_id']
        }

class CustomTokenRefreshSerializer(serializers.Serializer):
    """Custom token refresh serializer that preserves role"""
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        """Validate and include role in refresh response"""
        refresh = RefreshToken(attrs['refresh'])
        
        role = refresh.get('role', 'General')
        role_id = refresh.get('role_id', 3)  
        user_id = refresh.get('user_id')
        
        data = {'access': str(refresh.access_token)}
        
        data['role'] = role
        data['role_id'] = role_id
        data['user_id'] = user_id
        
        return data