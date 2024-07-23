
from toggl_python.api import ApiWrapper


class CurrentUser(ApiWrapper):
    prefix: str = "/me"

    def logged(self) -> bool:
        response = self.client.get(url=f"{self.prefix}/logged")
        _ = response.raise_for_status()

        # Returns 200 OK and empty response body
        return response.is_success
