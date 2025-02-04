"""Tests des instructions dans les cas où la réservation d'une place de
compétition doit aboutir.
 """

import server
from tests.utility_functions import (check_club_has_points_and_comp_has_places,
                                     check_competition_date_is_no_past,
                                     del_places_purchased_by_club_testing,
                                     reboot_json_tests, )


def test_booking_places_message_confirmation(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation possible :

    Test le message confirmant la réservation.
    """
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    expected_message = server.MESSAGE_GREAT_BOOKING

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert expected_message in response_summary.data.decode()

    reboot_json_tests()


def test_correct_deduction_of_number_places_to_comp(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation possible :

    Test que la déduction du nombre de places restantes de la compétition
    s'effectue correctement.
    """
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])
    numbers_of_places_comp_initial = int(competitions[0]["number_of_places"])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    response_summary = client.post("/showSummary", data=data_test)
    numbers_of_places_comp_final = int(competitions[0]["number_of_places"])

    assert response_purchase.status_code == 307
    assert response_summary.status_code == 200
    assert numbers_of_places_comp_final == (
            numbers_of_places_comp_initial - data_test["places"])

    reboot_json_tests()


def test_correct_deduction_of_points_club(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation possible :

    Test que la déduction du nombre de points restants du club s'effectue
    correctement.
    """
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])
    points_of_clubs_initial = int(clubs[0]["points"])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(clubs[0], competitions[0])
    }

    response_purchase = client.post("/purchasePlaces", data=data_test)
    points_of_clubs_final = int(clubs[0]["points"])

    assert response_purchase.status_code == 307
    assert points_of_clubs_final == (
            points_of_clubs_initial
            - data_test["places"] * server.RATIO_POINTS_PLACE
    )

    reboot_json_tests()

def test_add_places_purchases_by_club_if_zero_places_already(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation possible :

    Cas où le club n'a aucune réservation de places pour la compétition.
    Test que la réservation faite par le club est ajoutée aux données de la
    compétition.

    Nécessaire pour garder une trace du nombre de places réservées par le club
    et éviter qu'il ne réserve plus que le maximum autorisé par
    server.MAX_BOOK_PER_COMP_BY_CLUB.
    """
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

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
        data_test["places"])

    reboot_json_tests()


def test_update_places_purchase_by_clubs(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation possible :

    Cas où le club a déjà réservé au moins une place pour la compétition.
    Test que la réservation faite par le club est incrémentée aux données de la
    compétition.

    Nécessaire pour garder une trace du nombre de places réservées par le club
    et éviter qu'il ne réserve plus que le maximum autorisé par
    server.MAX_BOOK_PER_COMP_BY_CLUB.
    """
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
        int(value_club_places_initial_test) + data_test["places"])

    reboot_json_tests()
