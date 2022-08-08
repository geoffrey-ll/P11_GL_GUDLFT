import pytest

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    return client


@pytest.fixture
def mock_clubs(mocker):
    test_clubs = [
        {
            "name": "test club 01",
            "email": "test01@club.com",
            "points": "7"
        },
        {
            "name": "test club 02",
            "email": "test02@club.com",
            "points": "0"
        },
        {
            "name": "test club 03",
            "email": "test03@club.com",
            "points": "4"
        }
    ]
    mocked = mocker.patch.object(server, "clubs", test_clubs)
    yield mocked


@pytest.fixture
def mock_competitions(mocker):
    test_competitions = [
        {
            "name": "Test Festival",
            "date": "2021-11-06 08:00:00",
            "number_of_places": "9"
        },
        {
            "name": "Test competition",
            "date": "2019-01-25 13:30:00",
            "number_of_places": "13"
        }
    ]
    mocked = mocker.patch.object(server, "competitions", test_competitions)
    yield mocked
