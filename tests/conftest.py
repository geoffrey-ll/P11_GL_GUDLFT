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
            "name":"test club 01",
            "email":"test01@club.com",
            "points":"13"
        },
        {
            "name":"test club 02",
            "email":"test02@club.com",
            "points":"5"
        },
        {
            "name":"test club 03",
            "email":"test03@club.com",
            "points":"4"
        }
    ]
    mocked = mocker.patch.object(server, "clubs", test_clubs)
    yield mocked
