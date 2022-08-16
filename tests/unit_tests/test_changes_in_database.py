import server


from .utility_functions import (
    check_club_has_points_and_comp_has_places,
    check_competition_date_is_no_past,
    determine_maximum_booking
)


def test_correct_deduction_of_number_places_to_comp(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
            mock_clubs[0],
            mock_competitions[0]
        )
    check_competition_date_is_no_past(mock_competitions[0])
    numbers_of_places_comp_initial = int(
        mock_competitions[0]["number_of_places"]
    )

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": determine_maximum_booking(mock_clubs[0], mock_competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    numbers_of_places_comp_final = int(
            mock_competitions[0]["number_of_places"]
    )

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert numbers_of_places_comp_final == (
            numbers_of_places_comp_initial - data_test["places"]
    )


def test_correct_deduction_of_points_club(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    points_of_clubs_initial = int(mock_clubs[0]["points"])

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": determine_maximum_booking(mock_clubs[0], mock_competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    points_of_clubs_final = int(mock_clubs[0]["points"])

    assert response_purchase.status_code == 307
    assert points_of_clubs_final == (
            points_of_clubs_initial - data_test["places"]
    )


def test_writing_places_purchases_by_club_if_zero_places_already(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    if mock_clubs[0]["name"] in mock_competitions[0]["clubs_places"]:
        del mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]]

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 1
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]] == str(
        data_test["places"]
    )


def test_update_places_purchase_by_clubs(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    del mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]]
    value_club_places_initial_test = "4"
    mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]] = \
        value_club_places_initial_test

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 1
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]] == str(
        int(value_club_places_initial_test) + data_test["places"]
    )


def test_not_update_places_purchase_if_over_12(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]] = "12"

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 1
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
    assert mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]] == "12"
