from datetime import datetime
import json


from flask import Flask, render_template, request, redirect, flash, url_for


FILENAME_CLUBS = "clubs.json"
FILENAME_COMPETITIONS = "competitions.json"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


MESSAGE_ERROR_DATA_CLUBS = "The data of the clubs were not found."
MESSAGE_ERROR_DATA_COMPETITIONS = "The data of the competitions wer not found."
MESSAGE_ERROR_DISPLAY_BOOK_VIEW = "Something went wrong-please try again."
MESSAGE_ERROR_INPUT_PLACES = "Incorrect value."
MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB = "Maximum 12 places by club."
MESSAGE_ERROR_PAST_COMPETITION = "This competition is past. Booking is not " \
                                 "possible."
MESSAGE_NOT_BOOKING_POSSIBLE = "Impossible to booking places.\n" \
                               "Check points clubs, check number of places " \
                               "competitions and check number of places " \
                               "booked by club for this competition (max 12)."
MESSAGE_NOT_ENOUGH_POINTS = "You don't have enough points."
MESSAGE_NOT_ENOUGH_PLACES = "The competition doesn't have enough places."
MESSAGE_NOT_POINTS_CLUB = "You have no points to spend."
MESSAGE_NOT_PLACES_COMP = "The competition has no places."
MESSAGE_GREAT_BOOKING = "Great-booking complete!"
MESSAGE_INPUT_EMAIL_NONEXISTENT = "You have not transmitted the from " \
                                  "{email: votre@email.com}"
MESSAGE_INPUT_EMAIL_EMPTY = "Sorry, you have to fill in an email."
MESSAGE_INPUT_EMAIL_UNKNOWN = "Sorry, that email wasn't found."
MESSAGE_INPUT_PLACES_EMPTY = "Indicate the number of places to book."


app = Flask(__name__)
app.secret_key = "something_special"


def today():
    return datetime.now().strftime(DATETIME_FORMAT)


def load_clubs():
    with open(FILENAME_CLUBS) as c:
        list_of_clubs = json.load(c)["clubs"]
    c.close()
    return list_of_clubs


def load_competitions():
    with open(FILENAME_COMPETITIONS) as comps:
        list_of_competitions = json.load(comps)["competitions"]
    comps.close()
    return list_of_competitions


def load_database():
    global clubs, competitions
    clubs = load_clubs()
    competitions = load_competitions()
    return clubs, competitions


def update_database():
    with open(FILENAME_CLUBS, mode="w") as c:
        json.dump({"clubs": clubs}, c, indent=2)
    c.close()
    with open(FILENAME_COMPETITIONS, mode="w") as comps:
        json.dump({"competitions": competitions}, comps, indent=2)
    comps.close()


@app.route("/")
def index():
    load_database()
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    try:
        request_email = request.form["email"]
    except KeyError:
        flash(MESSAGE_INPUT_EMAIL_NONEXISTENT)
        return redirect(url_for("index"))

    try:
        club = [club for club in clubs if club["email"] == request_email][0]
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
        )
    except IndexError:
        if request_email == "":
            flash(MESSAGE_INPUT_EMAIL_EMPTY)
        else:
            flash(MESSAGE_INPUT_EMAIL_UNKNOWN)
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        found_club = [c for c in clubs if c["name"] == club][0]
    except NameError:
        found_club = False
        flash(MESSAGE_ERROR_DATA_CLUBS)
    try:
        found_competition = [
            c for c in competitions if c["name"] == competition
        ][0]
    except NameError:
        found_competition = False
        flash(MESSAGE_ERROR_DATA_COMPETITIONS)

    if found_club and found_competition:
        places_still_purchasable = 12
        if found_club["name"] in found_competition["clubs_places"]:
            places_still_purchasable = (
                    12 - int(found_competition["clubs_places"][found_club["name"]])
            )
        maximum_booking = min(
            int(found_club["points"]),
            int(found_competition["number_of_places"]),
            places_still_purchasable
        )

        comp_or_club_no_found = False
        comp_is_past = False
        maxi_is_zero = False
        if found_club == [] or found_competition == []:
            comp_or_club_no_found = True
            flash(MESSAGE_ERROR_DISPLAY_BOOK_VIEW)
        if found_competition["date"] < today():
            comp_is_past = True
            flash(MESSAGE_ERROR_PAST_COMPETITION)
        if maximum_booking == 0:
            maxi_is_zero = True
            flash(MESSAGE_NOT_BOOKING_POSSIBLE)

        errors = [comp_or_club_no_found, comp_is_past, maxi_is_zero]
        for error in errors:
            if error is True:
                return render_template(
                    "welcome.html",
                    club=found_club,
                    competitions=competitions,
                )

        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition,
            maximum_booking=maximum_booking
        )
    else:
        return redirect(url_for("index"))


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    places_form_empty = False
    if request.form["places"] == "":
        places_form_empty = True
        flash(MESSAGE_INPUT_PLACES_EMPTY)

    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    places_form_err = False
    try:
        places_required = int(request.form["places"])
    except ValueError:
        places_form_err = True
        flash(MESSAGE_ERROR_INPUT_PLACES)
        places_required = 0

    comp_is_past = False
    zero_points_club = False
    zero_places_comp = False
    over_12_required = False
    over_points_club = False
    over_places_comp = False
    over_12_with_old = False
    if competition["date"] < today():
        comp_is_past = True
        flash(MESSAGE_ERROR_PAST_COMPETITION)
    if int(club["points"]) == 0:
        zero_points_club = True
        flash(MESSAGE_NOT_POINTS_CLUB)
    if int(competition["number_of_places"]) == 0:
        zero_places_comp = True
        flash(MESSAGE_NOT_PLACES_COMP)
    if places_required > 12:
        over_12_required = True
        flash(MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB)
    if places_required > int(club["points"]):
        over_points_club = True
        flash(MESSAGE_NOT_ENOUGH_POINTS)
    if places_required > int(competition["number_of_places"]):
        over_places_comp = True
        flash(MESSAGE_NOT_ENOUGH_PLACES)
    if club["name"] in competition["clubs_places"]:
        total_temp = (
            int(competition["clubs_places"][club["name"]]) + places_required
        )
        if total_temp > 12:
            over_12_with_old = True
            flash(MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB)
    else:
        total_temp = places_required

    errors = [
        places_form_empty,
        places_form_err,
        comp_is_past,
        zero_points_club,
        zero_places_comp,
        over_12_required,
        over_points_club,
        over_places_comp,
        over_12_with_old
    ]

    # TODO : Il faut modifier les valeurs dans clubs et competitions !!
    # if (error for error in errors) is False:
    for error in errors:
        if error is True:
            return redirect(
                url_for(
                    "book",
                    competition=request.form["competition"],
                    club=request.form["club"]
                )
            )

    competition["clubs_places"][club["name"]] = str(total_temp)
    club["points"] = str(int(club["points"]) - places_required)
    competition["number_of_places"] = str(
        int(competition["number_of_places"]) - places_required
    )
    update_database()
    flash(MESSAGE_GREAT_BOOKING)
    return redirect(url_for("show_summary"), code=307)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
