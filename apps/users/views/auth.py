from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny

from utils.core.response_wrappers import OKResponse, BadResponse, UnauthorizedResponse
from ..serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

class TokenGenerateAPI(TokenObtainPairView):
    """
    Generate JWT tokens with user role in payload
    POST /users/tokens/generate/
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            data = serializer.validated_data
            
            return OKResponse(
                message="Login successful",
                data=data
            )
            
        except TokenError as e:
            return UnauthorizedResponse(
                message="Authentication failed",
                errors={"detail": str(e)}
            )
        except Exception as e:
            return BadResponse(
                message="Invalid credentials",
                errors={"detail": str(e)}
            )

class TokenRefreshAPI(TokenRefreshView):
    """
    Refresh JWT access token with role preservation
    POST /users/tokens/refresh/
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            data = serializer.validated_data
            
            return OKResponse(
                message="Token refreshed successfully",
                data=data
            )
            
        except TokenError as e:
            return UnauthorizedResponse(
                message="Token refresh failed",
                errors={"detail": str(e)}
            )
        except Exception as e:
            return BadResponse(
                message="Invalid token",
                errors={"detail": str(e)}
            )