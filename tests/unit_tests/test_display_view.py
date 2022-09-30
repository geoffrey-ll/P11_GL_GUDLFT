"""Test les views."""

import copy

import server
from .utility_functions import (check_club_has_points_and_comp_has_places,
                                check_competition_date_is_no_past,
                                del_places_purchased_by_club_testing,
                                test_clubs, test_competitions,)


def test_no_display_book_view_if_past_competition(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation impossible :

    Cas : Date de la compétition est passée.
    Le template booking.html ne doit pas être accessible.

    Test que le message d'erreur du template welcome.html est présent pour
    cette request vers la route book.
    """
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])
    competitions[0]["date"] = "1900-01-01 01:00:00"

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": 1
    }

    response_book = client.get(
        f"/book/{competitions[0]['name']}/{clubs[0]['name']}", data=data_test)
    expected_message = server.MESSAGE_ERROR_PAST_COMPETITION

    assert response_book.status_code == 200
    assert expected_message in response_book.data.decode()


def test_no_display_book_view_if_no_found_club_in_data(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation impossible :

    Cas : Données des clubs non trouvées.
    Le template booking.html ne doit pas être accessible.

    Test que le message d'erreur du template welcome.html est présent pour
    cette request vers la route book.
    """

    # Le chargement des json puis leurs suppressions de la mémoire est
    # important pour que le test passe s'il est lancé en même temps que
    # d'autres test chargeant les json.
    server.load_database()
    del server.clubs, server.competitions
    # Une copy profonde de test_clubs et de test_competitions est nécessaire
    # pour ne pas modifier en mémoire ces deux dictionnaires de références
    # utiles à d'autres tests.
    test_club_temp = copy.deepcopy(test_clubs[0])
    test_comp_temp = copy.deepcopy(test_competitions[0])

    check_club_has_points_and_comp_has_places(test_club_temp, test_comp_temp)
    check_competition_date_is_no_past(test_comp_temp)
    del_places_purchased_by_club_testing(test_club_temp, test_comp_temp)

    response_book = client.get(
        f"/book/{test_comp_temp['name']}/{test_club_temp['name']}",
        follow_redirects=True)
    expected_message = server.MESSAGE_ERROR_DATA_CLUBS_NO_FOUND

    assert response_book.status_code == 200
    assert expected_message in response_book.data.decode()


def test_no_display_book_view_if_no_found_competition_in_data(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation impossible :

    Cas : Données des compétitions non trouvées.
    Le template booking.html ne doit pas être accessible.

    Test que le message d'erreur du template welcome.html est présent pour
    cette request vers la route book.
    """

    # Le chargement des json puis leurs suppressions de la mémoire est
    # important pour que le test passe s'il est lancé en même temps que
    # d'autres test chargeant les json.
    server.load_database()
    del server.clubs, server.competitions
    # Une copy profonde de test_clubs et de test_competitions est nécessaire
    # pour ne pas modifier en mémoire ces deux dictionnaires de références
    # utiles à d'autres tests.
    test_club_temp = copy.deepcopy(test_clubs[0])
    test_comp_temp = copy.deepcopy(test_competitions[0])

    check_club_has_points_and_comp_has_places(test_club_temp, test_comp_temp)
    check_competition_date_is_no_past(test_comp_temp)
    del_places_purchased_by_club_testing(test_club_temp, test_comp_temp)

    response_book = client.get(
        f"/book/{test_comp_temp['name']}/{test_club_temp['name']}",
        follow_redirects=True)
    expected_message = server.MESSAGE_ERROR_DATA_COMPETITIONS_NO_FOUND

    assert response_book.status_code == 200
    assert expected_message in response_book.data.decode()


def test_no_display_book_view_is_maximum_booking_is_zero(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation impossible :

    Cas : Le maximum réservable est 0.
    Le template booking.html ne doit pas être accessible.

    Test que le message d'erreur du template welcome.html est présent pour
    cette request vers la route book.
    """
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    clubs[0]["points"] = "0"
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(clubs[0], competitions[0])
    }

    response_book = client.get(
        f"/book/{competitions[0]['name']}/{clubs[0]['name']}", data=data_test,
        follow_redirects=True)
    expected_message = server.MESSAGE_NOT_BOOKING_POSSIBLE

    assert response_book.status_code == 200
    assert expected_message in response_book.data.decode()


def test_no_display_book_view_is_maximum_booking_is_negative(
        client, mock_filename_clubs, mock_filename_competitions):
    """Réservation impossible :

    Cas : Le maximum réservable est négatif.
    Le template booking.html ne doit pas être accessible.

    Test que le message d'erreur du template welcome.html est présent pour
    cette request vers la route book.
    """
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    clubs[0]["points"] = "-20"
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])

    data_test ={
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(clubs[0], competitions[0])
    }

    response_book = client.get(
        f"/book/{competitions[0]['name']}/{clubs[0]['name']}", data=data_test,
        follow_redirects=True)
    expected_message = server.MESSAGE_ERROR_MAX_BOOKING_IS_NEGATIVE

    assert response_book.status_code == 200
    assert expected_message in response_book.data.decode()


def test_display_current_points_balance_clubs_in_points_board_view(
        client, mock_filename_clubs, mock_filename_competitions):
    """Test la présence de tous les noms de club et de leurs points dans le
    template points_board.html.
    """
    clubs, competitions = server.load_database()

    response_points_board = client.get(f"/pointsBoard", follow_redirects=True)
    expected_values_names = [club["name"] for club in clubs]
    expected_values_points = [club["points"] for club in clubs]

    assert response_points_board.status_code == 200
    for value_name in expected_values_names:
        assert value_name in response_points_board.data.decode()
    for value_points in expected_values_points:
        assert value_points in response_points_board.data.decode()
