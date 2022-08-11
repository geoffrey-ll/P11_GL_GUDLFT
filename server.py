import json


from flask import Flask, render_template, request, redirect, flash, url_for


MESSAGE_ERROR_DISPLAY_BOOK_VIEW = "Something went wrong-please try again."
MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB = "Maximum 12 places by club."
MESSAGE_NOT_ENOUGH_POINTS = "You don't have enough points."
MESSAGE_NOT_POINTS_CLUB = "You have no points to spend."
MESSAGE_GREAT_BOOKING = "Great-booking complete!"
MESSAGE_INPUT_PLACES_EMPTY = "Indicate the number of places to book."
MESSAGE_INPUT_EMAIL_UNKNOWN = "Sorry, that email wasn't found."
MESSAGE_INPUT_EMAIL_EMPTY = "Sorry, you have to fill in an email."


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

    maximum_booking = min(
        int(found_club["points"]),
        int(found_competition["number_of_places"]),
        12
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
    if request.form["places"] == "":
        flash(MESSAGE_INPUT_PLACES_EMPTY)
        return redirect(
            url_for(
                "book",
                competition=request.form["competition"],
                club=request.form["club"]
            )
        )

    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])

    over_12_required = False
    over_points_club = False
    zero_points_club = False
    over_12_with_old = False
    if places_required > 12:
        over_12_required = True
        flash(MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB)
    if places_required > int(club["points"]):
        over_points_club = True
        flash(MESSAGE_NOT_ENOUGH_POINTS)
    if int(club["points"]) == 0:
        zero_points_club = True
        flash(MESSAGE_NOT_POINTS_CLUB)
    if club["name"] in competition["clubs_places"]:
        total_temp = (
            int(competition["clubs_places"][club["name"]]) + places_required
        )
        if total_temp > 12:
            over_12_with_old = True
            flash(MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB)
    else:
        total_temp = places_required

    if over_12_required is True \
            or over_points_club is True \
            or zero_points_club is True \
            or over_12_with_old is True:
        return redirect(
            url_for(
                "book",
                competition=request.form["competition"],
                club=request.form["club"]
            )
        )

    # TODO : Il faut modifier les valeurs dans clubs et competitions !!
    if over_12_required is False \
            and over_points_club is False \
            and zero_points_club is False \
            and over_12_with_old is False:
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
