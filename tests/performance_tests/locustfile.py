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

    # @task#(6)
    # def index(self):
    #     print(f"\nTEST\n{GudlftPerfTest.index.__name__}\n")
    #     with self.client.get('/', catch_response=True) as response:
    #         if response.elapsed.total_seconds() > 5:
    #             response.failure(self.MESSAGE_TOO_LONG_RESPONSE)
    #     # Si pas de response ?
    #
    # @task
    # # Chargement < 5s
    # def show_summary(self):
    #     data_test = {"email": "john@simplylift.co"}
    #     with self.client.post(
    #             "/showSummary", data=data_test,
    #              catch_response=True) as response:
    #         if response.elapsed.total_seconds() > 5:
    #             response.failure(self.MESSAGE_TOO_LONG_RESPONSE)
    #
    # @task
    # def book(self):
    #     with self.client.get(
    #             "/book/Spring Festival/Simply Lift",
    #             catch_response=True) as response:
    #         if response.elapsed.total_seconds() > 5:
    #             response.failure(self.MESSAGE_TOO_LONG_RESPONSE)
    #
    #
    # @task
    # # Update json < 2s.
    # def purchase_place(self):
    #     data_test = {
    #         "club": "Simply Lift",
    #         "competition": "Fall Classic",
    #         "places": 1
    #     }
    #     with self.client.post(
    #             "/purchasePlaces", data=data_test,
    #             catch_response=True) as response:
    #         if response.elapsed.total_seconds() > 2:
    #             response.failure(self.MESSAGE_TOO_LONG_RESPONSE)
    #
    # @task
    # def points_board(self):
    #     with self.client.get("/pointsBoard", catch_response=True) as response:
    #         if response.elapsed.total_seconds() > 5:
    #             response.failure(self.MESSAGE_TOO_LONG_RESPONSE)
    #
    # @task
    # def logout(self):
    #     with self.client.get("/logout", catch_response=True) as response:
    #         if response.elapsed.total_seconds() > 5:
    #             response.failure(self.MESSAGE_TOO_LONG_RESPONSE)
