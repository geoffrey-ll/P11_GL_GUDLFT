def test_message_when_form_is_empty(client, mock_clubs, mock_competitions):
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": ""
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_book = client.get(
        f"/book/{data_test['competition']}/{data_test['club']}"
    )
    expected_value = "Indicate the number of places to book."

    assert response_purchase.status_code == 302
    assert response_book.status_code == 200
    assert expected_value in response_book.data.decode()


def test_message_when_spend_more_points_have_club(client, mock_clubs, mock_competitions):
    points_of_club = int(mock_clubs[0]["points"])
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 8
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_book = client.get(
        f"/book/{data_test['competition']}/{data_test['club']}"
    )
    expected_value = "You don&#39;t have enough points."

    assert points_of_club < data_test["places"]
    assert response_purchase.status_code ==  302
    assert response_book.status_code == 200
    assert expected_value in response_book.data.decode()


def test_message_when_club_no_points(client, mock_clubs, mock_competitions):
    datatest = {
        "email": mock_clubs[1]["email"],
        "club": mock_clubs[1]["name"],
        "competition": mock_competitions[1]["name"],
        "places": 1
    }

    response_purchase = client.post(f"/purchasePlaces", data=datatest)
    expected_value = "You have no points to spend."
    response_book = client.get(
        f"/book/{mock_competitions[0]['name']}/{mock_clubs[1]['name']}"
    )

    assert mock_clubs[1]["points"] == "0"
    assert response_purchase.status_code == 302
    assert expected_value in response_book.data.decode()


def test_message_confirm_spending_points(client, mock_clubs, mock_competitions):
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 6
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    expected_value = "Great-booking complete!"

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert expected_value in response_summary.data.decode()


def test_correct_deduction_of_number_places_to_comp(client, mock_clubs, mock_competitions):
    numbers_of_places_comp_initial = int(
        mock_competitions[0]["number_of_places"]
    )
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 2
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    numbers_of_places_comp_final = int(
        mock_competitions[0]["number_of_places"]
    )

    assert response_purchase.status_code == 307
    assert numbers_of_places_comp_final == (
            numbers_of_places_comp_initial - data_test["places"]
    )


def test_correct_deduction_of_points_club(client, mock_clubs, mock_competitions):
    points_of_clubs_initial =int(mock_clubs[0]["points"])
    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 5
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    points_of_clubs_final = int(mock_clubs[0]["points"])

    assert response_purchase.status_code == 307
    assert points_of_clubs_final == (
            points_of_clubs_initial - data_test["places"]
    )
