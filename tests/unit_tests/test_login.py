from flask import url_for

def test_login_with_unknown_email(client, mock_clubs):
    email = "inexistant@email.com"
    response = client.post("/showSummary", data={"email": email}, follow_redirects=True)
    expected_message = "Sorry, that email wasn&#39;t found."
    assert response.status_code == 200
    assert expected_message in response.data.decode()


def test_login_with_empty_email(client, mock_clubs):
    email = ""
    response = client.post("/showSummary", data={"email": email}, follow_redirects=True)
    expected_message = "Sorry, you have to fill in an email."
    assert response.status_code == 200
    assert expected_message in response.data.decode()


def test_login_with_a_known_email(client, mock_clubs):
    email = "test01@club.com"
    response = client.post("/showSummary", data={"email": email})
    expected_message = "test01"
    assert response.status_code == 200
    assert expected_message in response.data.decode()

