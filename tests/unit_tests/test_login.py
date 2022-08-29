import server


def test_login_with_unknown_email(client, mock_filename_clubs, mock_filename_competitions):
    server.load_database()

    data_test = {"email": "inexistant@email.com"}

    response_summary = client.post(
        "/showSummary",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_INPUT_EMAIL_UNKNOWN.replace("'", "&#39;")

    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()


def test_login_with_empty_email(client, mock_filename_clubs, mock_filename_competitions):
    server.load_database()

    data_test = {"email": ""}

    response_summary = client.post(
        "/showSummary",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_INPUT_EMAIL_EMPTY

    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()


def test_login_with_a_known_email(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    data_test = {"email": clubs[0]["email"]}

    response_summary = client.post("/showSummary", data=data_test)
    expected_message = data_test["email"]

    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()
