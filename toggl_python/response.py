class ListResponse(list):
    def __init__(self, value, response):
        super(ListResponse, self).__init__(value)

        data = response.json()
        self.total_count = data.get("total_count")
        self.per_page = data.get("per_page")
