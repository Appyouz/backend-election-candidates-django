# responses.py
from rest_framework.response import Response
from rest_framework import status


class OKResponse(Response):
    def __init__(self, *, message="Success", data=None, **kwargs):
        status_code = status.HTTP_200_OK
        response_data = {
            "data": data,
            "message": message,
            # "status": status_code,
        }
        super().__init__(data=response_data, status=status_code, **kwargs)


class CreatedResponse(Response):
    def __init__(self, *, message="Created", data=None, **kwargs):
        status_code = status.HTTP_201_CREATED
        response_data = {
            "data": data,
            "message": message,
            # "status": status_code,
        }
        super().__init__(data=response_data, status=status_code, **kwargs)


class NoContentResponse(Response):
    def __init__(self, *, message="Successful", data=None, **kwargs):
        status_code = status.HTTP_204_NO_CONTENT
        response_data = {
            "data": data,
            "message": message,
            # "status": status_code,
        }
        super().__init__(data=response_data, status=status_code, **kwargs)


class BadResponse(Response):
    def __init__(
        self,
        message="Bad Request",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        **kwargs
    ):
        errors = errors or {}
        response_data = {
            "message": message,
            "extra": errors,
            # "status": status_code,
        }
        super().__init__(data=response_data, status=status_code, **kwargs)


class UnauthorizedResponse(Response):
    def __init__(
        self,
        message="Unauthorized",
        errors=None,
        status_code=status.HTTP_401_UNAUTHORIZED,
        **kwargs
    ):
        errors = errors or {}
        response_data = {
            "message": message,
            "extra": errors,
            # "status": status_code,
        }
        super().__init__(data=response_data, status=status_code, **kwargs)
