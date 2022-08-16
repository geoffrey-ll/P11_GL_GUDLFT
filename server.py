from datetime import datetime
from time import strftime
import json


from flask import Flask, render_template, request, redirect, flash, url_for


MESSAGE_ERROR_DISPLAY_BOOK_VIEW = "Something went wrong-please try again."
MESSAGE_ERROR_INPUT_PLACES = "Incorrect value."
MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB = "Maximum 12 places by club."
MESSAGE_NOT_ENOUGH_POINTS = "You don't have enough points."
MESSAGE_NOT_ENOUGH_PLACES = "The competition doesn't have enough places."
MESSAGE_NOT_POINTS_CLUB = "You have no points to spend."
MESSAGE_NOT_PLACES_COMP = "The competition has no places."
MESSAGE_GREAT_BOOKING = "Great-booking complete!"
MESSAGE_INPUT_PLACES_EMPTY = "Indicate the number of places to book."
MESSAGE_INPUT_EMAIL_UNKNOWN = "Sorry, that email wasn't found."
MESSAGE_INPUT_EMAIL_EMPTY = "Sorry, you have to fill in an email."


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        c.close()
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        comps.close()
        return list_of_competitions


app = Flask(__name__)
app.secret_key = "something_special"


competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    request_email = request.form["email"]

    try:
        club = [club for club in clubs if club["email"] == request_email][0]
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions
        )
    except IndexError:
        if request_email == "":
            flash(MESSAGE_INPUT_EMAIL_EMPTY)
        else:
            flash(MESSAGE_INPUT_EMAIL_UNKNOWN)

        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [
        c for c in competitions if c["name"] == competition
    ][0]

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

    if found_club and found_competition:
        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition,
            maximum_booking=maximum_booking
        )
    else:
        flash(MESSAGE_ERROR_DISPLAY_BOOK_VIEW)
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions
        )


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


    zero_points_club = False
    zero_places_comp = False
    over_12_required = False
    over_points_club = False
    over_places_comp = False
    over_12_with_old = False
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

    flash(MESSAGE_GREAT_BOOKING)
    return redirect(url_for("show_summary"), code=307)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
