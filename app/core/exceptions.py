class BaseAppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ResourceNotFoundError(BaseAppError):
    pass


class ResourceAlreadyExistsError(BaseAppError):
    pass


class AuthenticationFailedError(BaseAppError):
    pass


class PermissionDeniedError(BaseAppError):
    pass
