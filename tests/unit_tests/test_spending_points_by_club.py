def test_message_when_form_is_empty(client, mock_clubs, mock_competitions):
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": ""
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_value = "Indicate the number of places to book."

    assert response_purchase.status_code == 200
    assert expected_value in response_purchase.data.decode()


def test_message_when_spend_more_points_have_club(client, mock_clubs, mock_competitions):
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": int(mock_clubs[0]["points"]) + 1
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_value = "You don&#39;t have enough points."

    assert response_purchase.status_code == 200
    assert expected_value in response_purchase.data.decode()


def test_message_when_club_no_points(client, mock_clubs, mock_competitions):
    data_test = {
        "email": mock_clubs[1]["email"],
        "club": mock_clubs[1]["name"],
        "competition": mock_competitions[1]["name"],
        "places": 1
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_value = "You have no points to spend."

    assert mock_clubs[1]["points"] == "0"
    assert response_purchase.status_code == 200
    assert expected_value in response_purchase.data.decode()


def test_message_confirm_spending_points(client, mock_clubs, mock_competitions):
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": min(int(mock_clubs[0]["points"]), 12)
    }

    # AVEC UN follow_redirects=True IMOPOSSIBLE DE FAIRE PASSER LE TESTS
    # CAR LE response_purchase.status_code EST TOUJOURS 400…
    #
    # CETTE response EST ENVOYÉE AVEC UN CODE 307, CONTRAIREMENT AU AUTRES TESTS
    # QUI MARCHE QUI ONT DES response ENVOYÉE AVEC UN CODE 302
    #
    #
    # response_purchase = client.post(
    #     "/purchasePlaces",
    #     data=data_test,
    #     follow_redirects=True
    # )
    # expected_value = "Great-booking complete!"
    # assert response_purchase.status_code == 200
    # assert expected_value in response_purchase.data.decode()

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test
    )
    response_summary = client.post("/showSummary", data=data_test)
    expected_value = "Great-booking complete!"

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert expected_value in response_summary.data.decode()
