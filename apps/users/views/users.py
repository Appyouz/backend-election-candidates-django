from rest_framework import generics, permissions
from rest_framework.views import APIView

from utils.core.response_wrappers import OKResponse, BadResponse
from ..models import User
from ..serializers import UserSerializer

class UserProfileAPI(APIView):
    """Get current user profile"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)
            
            return OKResponse(
                message="User profile retrieved successfully",
                data=serializer.data
            )
            
        except Exception as e:
            return BadResponse(
                message="Failed to retrieve user profile",
                errors={"detail": str(e)}
            )

class UserListAPI(generics.ListAPIView):
    """List users (admin only)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter users based on role permissions"""
        user = self.request.user
        
        if user.is_superuser:
            return User.objects.all()
        elif user.is_admin_user:
            return User.objects.exclude(role=User.Roles.SUPER)
        else:
            return User.objects.filter(id=user.id)
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            
            return OKResponse(
                message="Users retrieved successfully",
                data=response.data
            )
            
        except Exception as e:
            return BadResponse(
                message="Failed to retrieve users",
                errors={"detail": str(e)}
            )