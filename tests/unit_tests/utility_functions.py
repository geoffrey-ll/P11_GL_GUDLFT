from datetime import datetime, timedelta
import server


def determine_maximum_booking(club, competition):
    places_still_purchasable = 12
    if club["name"] in competition["clubs_places"]:
        places_still_purchasable = (
                12 - int(competition["clubs_places"][club["name"]])
        )
    maximum_booking = min(
        int(club["points"]),
        int(competition["number_of_places"]),
        places_still_purchasable
    )
    return maximum_booking


def check_club_has_points_and_comp_has_places(club, competition):
    if club["points"] == "0":
        club["points"] = "1"
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
