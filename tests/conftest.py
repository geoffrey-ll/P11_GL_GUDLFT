import pytest

import server


FILENAME_CLUBS_TEST = "./tests/clubs_test.json"
FILENAME_COMPETITION_TEST = "./tests/competitions_test.json"


@pytest.fixture
def client():
    """Configuration du client pour les tests."""
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    return client


@pytest.fixture
def mock_filename_clubs(mocker):
    """Mock du path du json des clubs, afin d'effectuer tous les tests avec un
    fichier spécifique.
    """
    mocked = mocker.patch("server.FILENAME_CLUBS", FILENAME_CLUBS_TEST)
    yield mocked


@pytest.fixture
def mock_filename_competitions(mocker):
    """Mock du path du json des compétitions, afin d'effectuer tous les tests
    avec un fichier spécifique.
    """
    mocked = mocker.patch(
        "server.FILENAME_COMPETITIONS", FILENAME_COMPETITION_TEST)
    yield mocked
