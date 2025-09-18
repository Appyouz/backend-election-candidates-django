from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# from rest_framework_api_key.permissions import HasAPIKey


class BaseAPIView(APIView):
    """
    Use PublicAPIView or AuthAPIView, don't use this directly
    """

    extra_permissions = []

    def get_permissions(self):
        return [
            permission()
            for permission in (self.permission_classes + self.extra_permissions)
        ]


class PublicAPIView(BaseAPIView):
    """
    Use this class to directly have a view that doesn't require authentication
    """

    extra_permissions = []
    # keeping authentication_classes empty allows requests without jwt token, invalid jwt or valid jwt token
    # would we ever need a condition where we need to allow request with invalid jwt?
    # for now, I'll comment below out.
    # authentication_classes = []
    permission_classes = []


class APIKeyAuthAPIView(BaseAPIView):
    extra_permissions = []
    # permission_classes = [HasAPIKey]


class AuthAPIView(BaseAPIView):
    """
    Use this class to directly have a view that requires authentication. For any extra permissions required, use extra_permissions = [IsSuper, ...]
    """

    extra_permissions = []
    permission_classes = [IsAuthenticated]


class TestAPIView(BaseAPIView):
    extra_permissions = []
    permission_classes = []
    # authentication_classes = []
