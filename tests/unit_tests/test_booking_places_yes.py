import server
from .utility_functions import (
    check_club_has_points_and_comp_has_places,
    check_competition_date_is_no_past,
    determine_maximum_booking,
    reboot_json_tests
)


def test_booking_places_message_confirmation(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    expected_message = server.MESSAGE_GREAT_BOOKING

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()

    reboot_json_tests()


def test_correct_deduction_of_number_places_to_comp(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    numbers_of_places_comp_initial = int(competitions[0]["number_of_places"])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    numbers_of_places_comp_final = int(competitions[0]["number_of_places"])

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert numbers_of_places_comp_final == (
            numbers_of_places_comp_initial - data_test["places"]
    )


def test_correct_deduction_of_points_club(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    points_of_clubs_initial = int(clubs[0]["points"])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    points_of_clubs_final = int(clubs[0]["points"])

    assert response_purchase.status_code == 307
    assert points_of_clubs_final == (
            points_of_clubs_initial - data_test["places"]
    )


def test_add_places_purchases_by_club_if_zero_places_already(
        client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    if clubs[0]["name"] in competitions[0]["clubs_places"]:
        del competitions[0]["clubs_places"][clubs[0]["name"]]

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": 1
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert competitions[0]["clubs_places"][clubs[0]["name"]] == str(
        data_test["places"]
    )


def test_update_places_purchase_by_clubs(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del competitions[0]["clubs_places"][clubs[0]["name"]]
    value_club_places_initial_test = "4"
    competitions[0]["clubs_places"][clubs[0]["name"]] = \
        value_club_places_initial_test

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": 1
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert competitions[0]["clubs_places"][clubs[0]["name"]] == str(
        int(value_club_places_initial_test) + data_test["places"]
    )
