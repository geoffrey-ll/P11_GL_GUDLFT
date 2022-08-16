import server
from .utility_functions import (
    check_club_has_points_and_comp_has_places,
    del_places_purchased_by_club_testing
)


def test_no_display_book_view_if_past_competition(client, mock_clubs, mock_competitions):
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

    response_book = client.get(
        f"/book/{mock_competitions[0]['name']}/{mock_clubs[0]['name']}",
        data=data_test,
        follow_redirects=True
    )
    expected_message = server.MESSAGE_ERROR_PAST_COMPETITION

    assert response_book.status_code == 200
    assert expected_message in response_book.data.decode()
