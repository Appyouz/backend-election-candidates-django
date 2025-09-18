class ApplicationError(Exception):
    """
    raise this to send 400 error. Look at utils/exception_handler.py
    """

    def __init__(self, message="There was an error", extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}


class InternalApplicationError(Exception):
    """
    raise this to send 500 error. Look at utils/exception_handler.py
    """

    def __init__(self, message="There was an error", extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}


class NotFoundError(Exception):
    """
    raise this to send 404 error. Look at utils/exception_handler.py
    """

    def __init__(self, message="Not Found", extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}


class DetailedValueError(ValueError):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field
