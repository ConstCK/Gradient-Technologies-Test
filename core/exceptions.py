class AppException(Exception):
    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(AppException):
    pass


class ValidationError(AppException):
    pass
