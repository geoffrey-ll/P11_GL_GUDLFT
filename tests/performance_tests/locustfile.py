from locust import HttpUser, task
from flask import url_for

# on_start()    on_stop()

class GudlftPerfTest(HttpUser):
    MESSAGE_TOO_LONG_RESPONSE = ""

    def test(self, method, path, time_over, data_test=None):
        if method == "GET":
            with self.client.get(f"{path}", catch_response=True) as response:
                if response.elapsed.total_seconds() > time_over:
                    response.failure(self.MESSAGE_TOO_LONG_RESPONSE)
        elif method == "POST":
            with self.client.post(f"{path}", data=data_test,
                                  catch_response=True) as response:
                if response.elapsed.total_seconds() > time_over:
                    response.failure(self.MESSAGE_TOO_LONG_RESPONSE)

    @task
    def index(self):
        self.test("GET", "/", 5)

    @task
    def show_summary(self):
        data_test = {"email": "john@simplylift.co"}
        self.test("POST", "/showSummary", 5, data_test=data_test)

    @task
    def book(self):
        self.test("GET", "/book/Spring Festival/Simply Lift", 5)

    @task
    def purchase_places(self):
        data_test = {
            "club": "Simply Lift",
            "competition": "Fall Classic",
            "places": 1
        }
        self.test("POST", "/purchasePlaces", 2, data_test)

    @task
    def points_boards(self):
        self.test("GET", "/pointsBoard", 5)

    @task
    def logout(self):
        self.test("GET", "/logout", 5)
