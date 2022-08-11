import server


def test_login_with_unknown_email(client, mock_clubs):
    email = "inexistant@email.com"
    response_summary = client.post(
        "/showSummary",
        data={"email": email},
        follow_redirects=True
    )
    expected_message = server.MESSAGE_INPUT_EMAIL_UNKNOWN.replace("'", "&#39;")
    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()


def test_login_with_empty_email(client, mock_clubs):
    email = ""
    response_summary = client.post(
        "/showSummary",
        data={"email": email},
        follow_redirects=True
    )
    expected_message = server.MESSAGE_INPUT_EMAIL_EMPTY
    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()


def test_login_with_a_known_email(client, mock_clubs):
    email = "test01@club.com"
    response_summary = client.post("/showSummary", data={"email": email})
    expected_message = email
    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()
