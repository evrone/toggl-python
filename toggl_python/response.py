from typing import Any, List, Tuple


class ListResponse(List[Any]):
    """
    Base class for list response based from mutable sequence
    """

    response_parameters: Tuple[str, ...] = ()

    def __init__(self, value: Any, response_body: Any):
        super(ListResponse, self).__init__(value)

        for parameter in self.response_parameters:
            if parameter in response_body:
                setattr(self, parameter, response_body[parameter])


class ReportTimeEntriesList(ListResponse):
    """
    Simple ListResponse, extended with params `response_parameters`
    from `response_body` on init
    """

    response_parameters = (
        "total_count",
        "per_page",
        "total_grand",
        "total_billable",
        "total_currencies",
    )
