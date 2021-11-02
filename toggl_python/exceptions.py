import httpx


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


class TooManyRequests(TogglException):
    pass


STATUS_2_EXCEPTION = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    429: TooManyRequests,
}


def raise_from_response(response: httpx.Response) -> None:
    """Raise exception based on the response status code."""
    if response.status_code < 400:
        return

    exception_cls = STATUS_2_EXCEPTION.get(response.status_code, TogglException)
    raise exception_cls(response.text)
