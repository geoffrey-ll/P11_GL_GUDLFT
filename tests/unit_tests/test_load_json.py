from .utility_functions import test_clubs, test_competitions
import server


def test_load_clubs_json(mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    assert clubs == test_clubs


def test_load_competitions_json(mock_filename_clubs, mock_filename_competitions):
    clubs, competitions = server.load_database()

    assert competitions == test_competitions
