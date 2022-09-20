import pytest

import server


FILENAME_CLUBS_TEST = "./tests/clubs_test.json"
FILENAME_COMPETITION_TEST = "./tests/competitions_test.json"


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    return client


@pytest.fixture
def mock_filename_clubs(mocker):
    mocked = mocker.patch("server.FILENAME_CLUBS", FILENAME_CLUBS_TEST)
    yield mocked


@pytest.fixtureFI
def mock_filename_competitions(mocker):
    mocked = mocker.patch(
        "server.FILENAME_COMPETITIONS", FILENAME_COMPETITION_TEST)
    yield mocked
