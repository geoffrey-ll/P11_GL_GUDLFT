"""Test la structure des données."""

from datetime import datetime

import server


def test_competition_datetime_format(
        mock_filename_clubs, mock_filename_competitions):
    """Vérifie le format d'horodatage des compétitions."""
    clubs, competitions = server.load_database()

    try:
        datetime.strptime(competitions[0]["date"], server.DATETIME_FORMAT)
        format_is_good = True
    except ValueError:
        format_is_good = False

    assert format_is_good is True
