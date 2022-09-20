from locust import HttpUser, task
from flask import url_for
from unittest import mock

# from ..conftest import mock_filename_clubs
# import server


# server.FILENAME_CLUBS = "./tests/clubs_test.json"


# on_start()    on_stop()

# @mock.patch("server.FILENAME_CLUBS", "tests/conftest.FILENAME_CLUBS_TEST")
class GudlftPerfTest(HttpUser):#mock_filename_clubs):

    def test_bal(self):
        print("ok")
        # print(f"\n{url_for('index')}\n")
        pass

    @task#(6)
    def task_access_index_page(self):
        self.test_bal()
        self.client.get("/")
        # self.client.get(url_for("index"))

    @task
    # Chargement < 5s
    def task_loading_time_show_summary(self):
        data_test = {"email": "john@simplylift.co"}
        data_test_test = {"email": "test01@club.com"}
        # self.client.post(url_for("showSummary"), data=data_test)
        self.client.post("/showSummary", data_test)
        self.client.post("/showSummary", data_test_test)

    @task
    # Update json < 2s.
    def task_writing_after_purchase_place(self):
        pass
