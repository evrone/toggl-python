class ListResponse(list):
    def __init__(self, value, response_body):
        super(ListResponse, self).__init__(value)

        response_parameters = (
            "total_count",
            "per_page",
            "total_grand",
            "total_billable",
            "total_currencies",
        )

        for parameter in response_parameters:
            if parameter in response_body:
                setattr(self, parameter, response_body[parameter])
