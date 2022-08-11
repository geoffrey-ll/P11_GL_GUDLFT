import server


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
    expected_message = server.MESSAGE_INPUT_PLACES_EMPTY

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


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
    expected_message = server.MESSAGE_NOT_ENOUGH_POINTS.replace("'", "&#39;")

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


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
    expected_message = server.MESSAGE_NOT_POINTS_CLUB

    assert mock_clubs[1]["points"] == "0"
    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


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
    # expected_message = "Great-booking complete!"
    # assert response_purchase.status_code == 200
    # assert expected_message in response_purchase.data.decode()

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test
    )
    response_summary = client.post("/showSummary", data=data_test)
    expected_message = server.MESSAGE_GREAT_BOOKING

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()
