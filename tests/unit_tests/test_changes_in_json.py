import copy


import server
from .utility_functions import (
    check_club_has_points_and_comp_has_places,
    check_competition_date_is_no_past,
    del_places_purchased_by_club_testing,
    determine_maximum_booking,
    reboot_json_tests,
)


def test_writing_the_updated_data_in_clubs_json(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    clubs_json_before = copy.deepcopy(clubs)

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    clubs_json_after, competitions = server.load_database()

    assert response_purchase.status_code == 307
    assert clubs_json_before != clubs_json_after

    reboot_json_tests()


def test_writing_the_updated_data_in_competitions_json(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    competitions_json_before = copy.deepcopy(competitions)

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    clubs, competitions_json_after = server.load_database()

    assert response_purchase.status_code == 307
    assert competitions_json_after != competitions_json_before

    reboot_json_tests()
