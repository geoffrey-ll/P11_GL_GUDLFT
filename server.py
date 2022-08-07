import json


from flask import Flask, render_template, request, redirect, flash, url_for


MESSAGE_ERROR_DISPLAY_BOOK_VIEW = "Something went wrong-please try again"
MESSAGE_NOT_ENOUGH_POINTS = "You don't have enough points."
MESSAGE_NOT_POINTS_CLUB = "You have no points to spend."
MESSAGE_GREAT_BOOKING = "Great-booking complete!"
MESSAGE_INPUT_PLACES_EMPTY = "Indicate the number of places to book."
MESSAGE_INPUT_EMAIL_UNKNOW = "Sorry, that email wasn't found."
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
            flash(MESSAGE_INPUT_EMAIL_UNKNOW)

        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [
        c for c in competitions if c["name"] == competition
    ][0]

    if found_club and found_competition:
        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition
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

    if places_required > int(club["points"]):
        if int(club["points"]) == 0:
            flash(MESSAGE_NOT_POINTS_CLUB)
        else:
            flash(MESSAGE_NOT_ENOUGH_POINTS)
        return redirect(
            url_for(
                "book",
                competition=request.form["competition"],
                club=request.form["club"]
            )
        )

    competition["number_of_places"] = str(
        int(competition["number_of_places"]) - places_required
    )
    club["points"] = str(int(club["points"]) - places_required)

    flash(MESSAGE_GREAT_BOOKING)
    return redirect(url_for("show_summary"), code=307)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
