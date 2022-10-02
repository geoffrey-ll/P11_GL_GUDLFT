import server
from tests.utility_functions import (check_club_has_points_and_comp_has_places,
                                     check_competition_date_is_no_past,
                                     del_places_purchased_by_club_testing,)


def test_complete_process(
        client, mock_filename_clubs, mock_filename_competitions):
    """Test d'intégration d'un parcours utilisateur complet."""

    # /
    response_index = client.get("/")
    expected_text_in_index = "Welcome to the GUDLFT Registration Portal!"
    # Les clubs eet les compétitions sont chargés avec server.load_database()
    # lors de la request vers la route index.
    clubs, competitions = server.clubs, server.competitions
    # Conditions pour pouvoir aboutir à une réservation, afin de garantir un
    # test solide.
    # Conditions appliquées dès le début, pour ne pas avoir à modifier les data
    # du test d'intégration en cours d'exécution.
    check_club_has_points_and_comp_has_places(clubs[0], competitions[0])
    check_competition_date_is_no_past(competitions[0])
    del_places_purchased_by_club_testing(clubs[0], competitions[0])
    assert response_index.status_code == 200
    assert expected_text_in_index in response_index.data.decode()

    # /pointsBoard
    response_points_board = client.get("/pointsBoard")
    expected_clubs_names_in_points_board = [club["name"] for club in clubs]
    expected_clubs_points_in_points_board = [club["points"] for club in clubs]
    assert response_points_board.status_code == 200
    for value_name in expected_clubs_names_in_points_board:
        assert value_name in response_points_board.data.decode()
    for value_points in expected_clubs_points_in_points_board:
        assert value_points in response_points_board.data.decode()

    # /showSummary
    data_test_show_summary = {"email": clubs[0]["email"]}
    response_show_summary = client.post("/showSummary",
                                        data=data_test_show_summary)
    expected_club_email_in_show_summary = data_test_show_summary["email"]
    assert response_show_summary.status_code == 200
    assert (expected_club_email_in_show_summary
            in response_show_summary.data.decode())

    # /book/<competition>/<club>
    response_book = client.get(
        f"/book/{competitions[0]['name']}/{clubs[0]['name']}")
    expected_name_comp_in_book = competitions[0]["name"]
    expected_places_available_in_book = f"Places available: " \
                                     f"{competitions[0]['number_of_places']}"
    expected_text_in_book = "How many places?"
    assert response_book.status_code == 200
    assert (expected_name_comp_in_book
            and expected_places_available_in_book
            and expected_text_in_book) in response_book.data.decode()

    # /purchasePlaces
    data_test_purchase = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": server.determine_maximum_booking(clubs[0], competitions[0])
    }
    response_purchase = client.post("/purchasePlaces", data=data_test_purchase,
                                    follow_redirects=True)
    expected_message_in_purchase = server.MESSAGE_GREAT_BOOKING
    assert response_purchase.status_code == 200
    assert expected_message_in_purchase in response_purchase.data.decode()

    # logout
    response_logout = client.get("/logout", follow_redirects=True)
    assert response_logout.status_code == 200
    assert expected_text_in_index in response_logout.data.decode()
