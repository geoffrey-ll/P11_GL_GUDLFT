import server
from .utility_functions import (
    check_club_has_points_and_comp_has_places,
    check_competition_date_is_no_past,
    del_places_purchased_by_club_testing,
)

def test_no_booking_if_points_club_is_less_than_ratio_points_place(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    clubs[0]["points"] = "2"
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": (
                server.determine_maximum_booking(clubs[0], competitions[0]) + 1
        )
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_NOT_ENOUGH_POINTS.replace("'", "&#39;")

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
    pass


def test_no_booking_if_points_club_is_zero(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    clubs[0]["points"] = "0"
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
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
    assert clubs[0]["name"] not in competitions[0]["clubs_places"]


def test_no_booking_if_points_club_is_negative(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    clubs[0]["points"] = str(-server.RATIO_POINTS_PLACE)
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": int(clubs[0]["points"])
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_DATA_CLUB_POINTS_NEGATIVE

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_no_booking_if_places_comp_is_zero(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    competitions[0]["number_of_places"] = "0"
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(
            clubs[0],
            competitions[0]
        )
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_NOT_PLACES_COMP

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_no_booking_if_places_comp_is_negative(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    competitions[0]["number_of_places"] = "-1"
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": 1
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_DATA_COMPETITION_PLACES_NEGATIVE

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_no_booking_if_places_form_over_max_places_per_comp_by_club(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_competition_date_is_no_past(competitions[0])
    if int(clubs[0]["points"]) < 13:
        clubs[0]["points"] = "13"
    if int(competitions[0]["number_of_places"]) < 13:
        competitions[0]["number_of_places"] = "13"
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": 13,
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
    assert clubs[0]["name"] not in competitions[0]["clubs_places"]


def test_no_booking_if_places_form_over_points_club(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    if int(clubs[0]["points"]) >= 12 * server.RATIO_POINTS_PLACE:
        clubs[0]["points"] = "1"
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": int(clubs[0]["points"]) // server.RATIO_POINTS_PLACE + 1
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_NOT_ENOUGH_POINTS.replace("'", "&#39;")

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
    assert clubs[0]["name"] not in competitions[0]["clubs_places"]


def test_no_booking_if_places_form_over_places_comp(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": int(competitions[0]["number_of_places"]) + 1
    }
    if int(clubs[0]["points"]) < (
            int(data_test["places"]) * server.RATIO_POINTS_PLACE
    ):
        clubs[0]["points"] = data_test["places"]

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_NOT_ENOUGH_PLACES.replace("'", "&#39;")

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()


def test_no_booking_if_sum_places_form_and_club_places_over_max_places_per_comp_by_club(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    competitions[0]["clubs_places"][clubs[0]["name"]] = \
            server.MAX_BOOK_PER_COMP_BY_CLUB

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
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
    assert competitions[0]["clubs_places"][clubs[0]["name"]] == \
            server.MAX_BOOK_PER_COMP_BY_CLUB


def test_no_booking_if_places_form_no_int(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
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


def test_no_booking_if_places_form_empty(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
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


def test_no_booking_if_past_competition(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    competitions[0]["date"] = "1900-01-01 01:00:00"
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
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


def test_no_booking_if_club_places_is_negative(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])
    competitions[0]["clubs_places"][clubs[0]["name"]] = "-1"

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post(
        "/purchasePlaces",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_DATA_CLUB_PLACES_NEGATIVE

    assert response_purchase.status_code == 200
    assert expected_message in response_purchase.data.decode()
