from locust import HttpUser, task


class GudlftPerfTest(HttpUser):
    MESSAGE_TOO_LONG_RESPONSE = "The request takes too long."

    def perf_get_request(self, path, time_over):
        with self.client.get(f"{path}", catch_response=True) as response:
            if response.elapsed.total_seconds() > time_over:
                response.failure(self.MESSAGE_TOO_LONG_RESPONSE)

    def perf_post_request(self, path, time_over, data_test):
        with self.client.post(f"{path}", data=data_test,
                              catch_response=True) as response:
            if response.elapsed.total_seconds() > time_over:
                response.failure(self.MESSAGE_TOO_LONG_RESPONSE)

    @task
    def index(self):
        self.perf_get_request("/", 5)

    @task
    def show_summary(self):
        data_test = {"email": "john@simplylift.co"}
        self.perf_post_request("/showSummary", 5, data_test=data_test)

    @task
    def book(self):
        self.perf_get_request("/book/Spring Festival/Simply Lift", 5)

    @task
    def purchase_places(self):
        data_test = {
            "club": "Simply Lift",
            "competition": "Fall Classic",
            "places": 1
        }
        self.perf_post_request("/purchasePlaces", 2, data_test)

    @task
    def points_boards(self):
        self.perf_get_request("/pointsBoard", 5)

    @task
    def logout(self):
        self.perf_get_request("/logout", 5)
