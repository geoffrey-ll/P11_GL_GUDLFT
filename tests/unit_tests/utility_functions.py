from unittest import mock
from datetime import datetime, timedelta

import server


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

test_competitions = [
    {
        "name": "Test Festival",
        "date": "2021-11-06 08:00:00",
        "number_of_places": "9",
        "clubs_places": {
            "test club 01": "4",
            "test club 03": "7"
        }
    },
    {
        "name": "Test competition",
        "date": "2019-01-25 13:30:00",
        "number_of_places": "13",
        "clubs_places": {
            "test club 02": "6",
            "test club 01": "5"
        }
    }
]


def check_club_has_points_and_comp_has_places(club, competition):
    if club["points"] < str(server.RATIO_POINTS_PLACE):
        club["points"] = str(server.RATIO_POINTS_PLACE)
    if competition["number_of_places"] == "0":
        competition["number_of_places"] = "1"
    return club, competition


def check_competition_date_is_no_past(competition):
    today = datetime.now().strftime(server.DATETIME_FORMAT)
    today_temp = datetime.strptime(today, server.DATETIME_FORMAT)
    date_comp = datetime.strptime(competition["date"], server.DATETIME_FORMAT)
    if date_comp < today_temp:
        competition["date"] = str(today_temp + timedelta(days=7))
    return competition


def del_places_purchased_by_club_testing(club, competition):
    if club["name"] in competition["clubs_places"]:
        del competition["clubs_places"][club["name"]]
    return club, competition


@mock.patch("server.clubs", test_clubs)
@mock.patch("server.competitions", test_competitions)
def reboot_json_tests():
    return server.update_database()
