from http.client import HTTPException

from werkzeug.exceptions import BadRequest, Forbidden, UnprocessableEntity

# pylint: disable=no-member


class BaseError(HTTPException):

    message = "Unknown Error"
    error_code = "GENERIC_ERROR"

    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.message = message

    def __str__(self):
        code = self.code if self.code else "???"
        return f"{self.__class__.__name__} {code}: {self.description}, message: {self.message}"

    def __repr__(self):
        return self.__str__()


class UnprocessableError(BaseError):

    description = "The server encounterted an unexpected condition."
    code = UnprocessableEntity.code


class FileSizeError(BaseError):
    description = "File size bigger than allowed threshold"
    code = BadRequest.code


class FileExtnError(BaseError):
    description = "File extension not allowed"
    code = BadRequest.code


class AdminOnly(BaseError):
    description = "Only Admin Allowed to access the resource"
    code = Forbidden.code
