from toggl_python.api import ApiWrapper
from toggl_python.schemas.current_user import MeResponse, MeResponseWithRelatedData


class CurrentUser(ApiWrapper):
    prefix: str = "/me"

    def logged(self) -> bool:
        response = self.client.get(url=f"{self.prefix}/logged")
        _ = response.raise_for_status()

        # Returns 200 OK and empty response body
        return response.is_success

    def me(self, with_related_data: bool = False) -> MeResponse:
        response_schema = MeResponseWithRelatedData if with_related_data else MeResponse
        response = self.client.get(
            url=self.prefix, params={"with_related_data": with_related_data},
        )
        _ = response.raise_for_status()

        response_body = response.json()

        return response_schema.model_validate(response_body)
