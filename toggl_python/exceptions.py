class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass


class NotFound(Exception):
    pass


class MethodNotAllowed(Exception):
    pass


class NotSupported(Exception):
    pass


STATUS_2_EXCEPTION = {
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
}
