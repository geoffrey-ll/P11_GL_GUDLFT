import server


def test_no_login_if_form_email_nonexistent(client, mock_filename_clubs, mock_filename_competitions):
    response_summary = client.post("/showSummary", follow_redirects=True)
    expected_message = server.MESSAGE_INPUT_EMAIL_NONEXISTENT

    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()


def test_no_login_unknown_email(client, mock_filename_clubs, mock_filename_competitions):
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


def test_no_login_if_empty_email(client, mock_filename_clubs, mock_filename_competitions):
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


def test_login_if_a_known_email(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    data_test = {"email": clubs[0]["email"]}

    response_summary = client.post("/showSummary", data=data_test)
    expected_message = data_test["email"]

    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()


def test_logout(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    response_logout = client.get("/logout", follow_redirects=True)

    assert response_logout.status_code == 200
