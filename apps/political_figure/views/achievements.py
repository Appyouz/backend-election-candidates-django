from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from utils.core.permissions import IsAdminOrSuper
from ..models.achievements import Achievement
from ..serializers import AchievementSerializer

class AchievementViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Political Figure Achievements.
    """
    queryset = Achievement.objects.select_related('political_figure').all()
    serializer_class = AchievementSerializer
    
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the view requires.
        GET requests (list/retrieve) are read-only for anyone.
        POST, PATCH, DELETE require Admin or Super role.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny] 
        else:
            permission_classes = [IsAdminOrSuper] 
        return [permission() for permission in permission_classes]

    @extend_schema(summary="List all Achievements or filter by figure_id")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Create a new Achievement (Admin/Super Only)")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
