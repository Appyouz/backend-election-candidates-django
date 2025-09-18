# responses.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error

from .exceptions import ApplicationError, InternalApplicationError, NotFoundError
from django.http import Http404


def custom_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {},
    }

    # note: Taken from https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#errors--exception-handling

    """
    # print(type(exc))
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)
    # Handle Http404
    if isinstance(exc, Http404):
        response.data["message"] = "Not found"
        response.data["extra"] = response.data["detail"]
        # response.data["status"] = status.HTTP_404_NOT_FOUND
        del response.data["detail"]
        return response

    # If unexpected error occurs (server error, etc.)
    if response is None:
        # our custom error
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra,
                # "status": status.HTTP_400_BAD_REQUEST,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(exc, NotFoundError):
            data = {"message": exc.message, "extra": exc.extra}
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        # CRITICAL: FOR INTERNAL_APPLICATION_ERROR later on suppress this as to not send error detail to frontend
        if isinstance(exc, InternalApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra,
                # "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response
    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {"fields": response.data["detail"]}
        # response.data["status"] = status.HTTP_400_BAD_REQUEST

    # handle rest_framework_simplejwt.exceptions.InvalidToken
    # InvalidToken is subclass of exceptions.AuthenticationFailed and DetailDictMixin
    # from rest_framework_simplejwt.exceptions import InvalidToken
    elif isinstance(exc, exceptions.AuthenticationFailed):
        response.data["message"] = "Authentication Failed"
        response.data["extra"] = response.data["detail"]
        # response.data["status"] = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, exceptions.NotAuthenticated):
        # IMP: rest_framework does not raise 401 for NotAuthenticated() but raises 403.
        # That means it becomes impossible for client to know if
        # - it was unauthenticated and was trying to access a protected API
        # - it was authenticated but does not have permission to access that API
        # Because PermissionDenied() and NotAuthenticated() both give 403.
        # For more resources:
        # https://github.com/encode/django-rest-framework/issues/5968 (they say it was intentional, but it does not make sense to me)
        # https://www.django-rest-framework.org/api-guide/authentication/#unauthorized-and-forbidden-responses
        # https://chatgpt.com/share/687b5d8a-f4e4-8009-be5a-e4baf4b587bf (chat with ChatGPT)

        # And if you're wondering why I simply did not do response.status_code = status.HTTP_401_UNAUTHORIZED, I just wanted to directly return the Response. Idk, it felt like overriding status_code attribute from the base class is not a good idea.

        # Another thing, the NotAuthenticated() is actually raised by APIView.permission_denied() and over there it should give 401, but inspecting in rest_framework.views.exception_handler already shows that it gives 403. Idk why that is and I don't want to know right now. I've spent way too much time on this. Goddamn. Right now I need to wrap up the project and show it to dai tomorrow, but I have so much work to do. 2025-07-19
        data = {
            "message": "Not authenticated",
            "extra": response.data["detail"],
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    elif isinstance(exc, exceptions.PermissionDenied):
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}
        # response.data["status"] = exc.status_code
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}
        # response.data["status"] = status.HTTP_400_BAD_REQUEST

    del response.data["detail"]
    return response
