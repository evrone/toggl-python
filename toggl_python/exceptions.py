class TogglException(Exception):
    pass


class BadRequest(TogglException):
    pass


class Unauthorized(TogglException):
    pass


class Forbidden(TogglException):
    pass


class NotFound(TogglException):
    pass


class MethodNotAllowed(TogglException):
    pass


class NotSupported(TogglException):
    pass


STATUS_2_EXCEPTION = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
}
