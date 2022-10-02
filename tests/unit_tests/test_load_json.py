"""Test du chargement des données."""

import server
from tests.utility_functions import test_clubs, test_competitions


def test_load_clubs_json(mock_filename_clubs, mock_filename_competitions):
    """Test le chargement des données des clubs."""
    clubs, competitions = server.load_database()

    assert clubs == test_clubs


def test_load_competitions_json(
        mock_filename_clubs, mock_filename_competitions):
    """Test le chargement des données des compétitions."""
    clubs, competitions = server.load_database()

    assert competitions == test_competitions
