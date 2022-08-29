import server
from .utility_functions import (
    check_club_has_points_and_comp_has_places,
    del_places_purchased_by_club_testing
)


def test_no_display_book_view_if_past_competition(client, mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    check_club_has_points_and_comp_has_places(
        clubs[0],
        competitions[0]
    )
    del_places_purchased_by_club_testing(clubs[0], competitions[0])
    competitions[0]["date"] = "1900-01-01 01:00:00"

    data_test = {
        "email": clubs[0]["email"],
        "club": clubs[0]["name"],
        "competition": competitions[0]["name"],
        "places": 1
    }

    response_book = client.get(
        f"/book/{competitions[0]['name']}/{clubs[0]['name']}",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_PAST_COMPETITION

    assert response_book.status_code == 200
    assert expected_message in response_book.data.decode()
