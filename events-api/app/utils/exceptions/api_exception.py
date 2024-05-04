from app.schemas.error import APIError


class APIException(Exception):
    def __init__(self, message: str, error: APIError):
        # Call the base exception class constructor with the parameters it needs
        super().__init__(message)

        self.error = error
