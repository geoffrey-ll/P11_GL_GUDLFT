def maximum_booking(club, competition):
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


def del_places_purchased_by_club_testing(club, competition):
    if club["name"] in competition["clubs_places"]:
        del competition["clubs_places"][club["name"]]
    return club, competition
