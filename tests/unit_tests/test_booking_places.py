import server


from .utility_functions import (
    check_club_has_points_and_comp_has_places,
    check_competition_date_is_no_past,
    del_places_purchased_by_club_testing,
    determine_maximum_booking
)


def test_no_booking_if_points_club_is_zero(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    mock_clubs[0]["points"] = "0"
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])

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
    expected_message = server.MESSAGE_NOT_POINTS_CLUB

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
    assert mock_clubs[0]["name"] not in mock_competitions[0]["clubs_places"]


def test_no_booking_if_places_comp_is_zero(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    mock_competitions[0]["number_of_places"] = "0"
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": determine_maximum_booking(mock_clubs[0], mock_competitions[0])
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_NOT_PLACES_COMP

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_no_booking_if_places_form_over_12(client, mock_clubs, mock_competitions):
    check_competition_date_is_no_past(mock_competitions[0])
    if int(mock_clubs[0]["points"]) < 13:
        mock_clubs[0]["points"] = "13"
    if int(mock_competitions[0]["number_of_places"]) < 12:
        mock_competitions[0]["number_of_places"] = "13"
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": 13,
    }

    response_purchase = client.post("/purchasePlaces", data=data_test, follow_redirects=True)
    expected_message = server.MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
    assert mock_clubs[0]["name"] not in mock_competitions[0]["clubs_places"]


def test_no_booking_if_places_form_over_points_club(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    if int(mock_clubs[0]["points"]) >= 12:
        mock_clubs[0]["points"] = "1"
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])

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
    assert mock_clubs[0]["name"] not in mock_competitions[0]["clubs_places"]


def test_no_booking_if_places_form_over_places_comp(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": int(mock_competitions[0]["number_of_places"]) + 1
    }
    if int(mock_clubs[0]["points"]) < data_test["places"]:
        mock_clubs[0]["points"] = data_test["places"]

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_NOT_ENOUGH_PLACES.replace("'", "&#39;")

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_no_booking_if_sum_places_form_and_club_places_over_12(client, mock_clubs, mock_competitions):
    check_competition_date_is_no_past(mock_competitions[0])
    if mock_clubs[0]["name"] not in mock_competitions[0]["clubs_places"] \
            or int(mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]]) > 12:
        mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]] = "7"
    places_already_purchase = \
        mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]]
    places_to_purchase = 12 - int(places_already_purchase) + 1
    if int(mock_clubs[0]["points"]) < places_to_purchase:
        mock_clubs[0]["points"] = places_to_purchase
    if int(mock_competitions[0]["number_of_places"]) < places_to_purchase:
        mock_competitions[0]["number_of_places"] = places_to_purchase

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": places_to_purchase
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
    assert mock_competitions[0]["clubs_places"][mock_clubs[0]["name"]] == \
           places_already_purchase


def test_no_booking_if_places_form_no_int(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": "a"
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_INPUT_PLACES

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_no_booking_if_places_form_empty(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])

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


def test_no_booking_if_past_competition(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    del_places_purchased_by_club_testing(mock_clubs[0], mock_competitions[0])
    mock_competitions[0]["date"] = "1900-01-01 01:00:00"

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
    expected_message = server.MESSAGE_ERROR_PAST_COMPETITION

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_booking_places_message_confirmation(client, mock_clubs, mock_competitions):
    check_club_has_points_and_comp_has_places(
        mock_clubs[0],
        mock_competitions[0]
    )
    check_competition_date_is_no_past(mock_competitions[0])

    data_test = {
        "email": mock_clubs[0]["email"],
        "club": mock_clubs[0]["name"],
        "competition": mock_competitions[0]["name"],
        "places": determine_maximum_booking(mock_clubs[0], mock_competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    expected_message = server.MESSAGE_GREAT_BOOKING

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()
