from datetime import datetime
import json

from decouple import config
from flask import flash, Flask, redirect, render_template, request, url_for


RATIO_POINTS_PLACE = 3
MAX_BOOK_PER_COMP_BY_CLUB = 12
FILENAME_CLUBS = "clubs.json"
FILENAME_COMPETITIONS = "competitions.json"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


MESSAGE_ERROR_DATA_CLUBS_NO_FOUND = "The data of the clubs were not found."
MESSAGE_ERROR_DATA_CLUB_POINTS_NEGATIVE = \
    "Your points balance is negative. Please contact an administrator."
MESSAGE_ERROR_DATA_COMPETITIONS_NO_FOUND = \
    "The data of the competitions wer not found."
MESSAGE_ERROR_DATA_COMPETITION_PLACES_NEGATIVE = \
    "Number of places in the competition is negative. " \
    "Please contact an administrator."
MESSAGE_ERROR_DATA_CLUB_PLACES_NEGATIVE = \
    "Places club already booked on this competition is negative. " \
    "Please contact an administrator."
MESSAGE_ERROR_MAX_BOOKING_IS_NEGATIVE = \
    "The maximum booking places is negative. Please contact an administrator."
MESSAGE_ERROR_DISPLAY_BOOK_VIEW = "Something went wrong-please try again."
MESSAGE_ERROR_INPUT_PLACES = "Incorrect value. Use only numbers"
MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB = "Maximum 12 places by club."
MESSAGE_ERROR_PAST_COMPETITION = \
    "This competition is past. Booking is not possible."
MESSAGE_NOT_BOOKING_POSSIBLE = \
    "Impossible to booking places.\nCheck points clubs, check number of " \
    "places competitions and check number of places booked by club for this " \
    "competition (max 12)."
MESSAGE_NOT_ENOUGH_POINTS = \
    "You don't have enough points.\n " \
    "Three points are required to booking one place."
MESSAGE_NOT_ENOUGH_PLACES = "The competition doesn't have enough places."
MESSAGE_NOT_POINTS_CLUB = "You have no points to spend."
MESSAGE_NOT_PLACES_COMP = "The competition has no places."
MESSAGE_GREAT_BOOKING = "Great-booking complete!"
MESSAGE_INPUT_EMAIL_NONEXISTENT = \
    "You have not transmitted the from {email: votre@email.com}"
MESSAGE_INPUT_EMAIL_EMPTY = "Sorry, you have to fill in an email."
MESSAGE_INPUT_EMAIL_UNKNOWN = "Sorry, that email wasn't found."
MESSAGE_INPUT_PLACES_EMPTY = "Indicate the number of places to book."
MESSAGE_INPUT_PLACES_NEGATIVE = "Enter a positive value."


app = Flask(__name__)
app.secret_key = config("SECRET_KEY")


def today():
    """Renvoi la date-temps au format attendu."""
    return datetime.now().strftime(DATETIME_FORMAT)


def load_clubs():
    """Chargement des données des clubs."""
    with open(FILENAME_CLUBS) as c:
        list_of_clubs = json.load(c)["clubs"]
    c.close()
    return list_of_clubs


def load_competitions():
    """Chargement des données des compétitions."""
    with open(FILENAME_COMPETITIONS) as comps:
        list_of_competitions = json.load(comps)["competitions"]
    comps.close()
    return list_of_competitions


def load_database():
    """Chargement des données (clubs et compétitions)."""
    global clubs, competitions
    clubs = load_clubs()
    competitions = load_competitions()
    return clubs, competitions


def update_database():
    """Mise à jour des données (clubs et compétitions)."""
    with open(FILENAME_CLUBS, mode="w") as c:
        json.dump({"clubs": clubs}, c, indent=2)
    c.close()

    with open(FILENAME_COMPETITIONS, mode="w") as comps:
        json.dump({"competitions": competitions}, comps, indent=2)
    comps.close()


def determine_maximum_booking(club_logged, competition_desired):
    """Calcul le maximum de places réservables par le club."""
    places_still_purchasable = MAX_BOOK_PER_COMP_BY_CLUB
    if club_logged["name"] in competition_desired["clubs_places"]:
        places_still_purchasable = (
                MAX_BOOK_PER_COMP_BY_CLUB
                - int(competition_desired["clubs_places"][club_logged["name"]]))
    maximum_booking = min(int(club_logged["points"]) // RATIO_POINTS_PLACE,
                          int(competition_desired["number_of_places"]),
                          places_still_purchasable)
    return maximum_booking


@app.route("/")
def index():
    """Page d'accueil du site."""
    load_database()
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """Page de sommaire après connexion de l'utilisateur."""
    try:
        request_email = request.form["email"]
    except KeyError:
        flash(MESSAGE_INPUT_EMAIL_NONEXISTENT)
        return redirect(url_for("index"))

    try:
        club = [club for club in clubs if club["email"] == request_email][0]
        return render_template("welcome.html", club=club,
                               competitions=competitions)
    except IndexError:
        if request_email == "":
            flash(MESSAGE_INPUT_EMAIL_EMPTY)
        else:
            flash(MESSAGE_INPUT_EMAIL_UNKNOWN)
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Page de booking d'une compétition."""
    try:
        found_club = [c for c in clubs if c["name"] == club][0]
    except NameError:
        found_club = False
        flash(MESSAGE_ERROR_DATA_CLUBS_NO_FOUND)
    try:
        found_competition = [
            c for c in competitions if c["name"] == competition
        ][0]
    except NameError:
        found_competition = False
        flash(MESSAGE_ERROR_DATA_COMPETITIONS_NO_FOUND)

    if found_club and found_competition:
        maximum_booking = determine_maximum_booking(found_club,
                                                    found_competition)
        comp_is_past = False
        maxi_is_zero = False
        maxi_is_nega = False
        if found_competition["date"] < today():
            comp_is_past = True
            flash(MESSAGE_ERROR_PAST_COMPETITION)
        if maximum_booking == 0:
            maxi_is_zero = True
            flash(MESSAGE_NOT_BOOKING_POSSIBLE)
        elif maximum_booking < 0:
            maxi_is_nega = True
            flash(MESSAGE_ERROR_MAX_BOOKING_IS_NEGATIVE)

        errors = [comp_is_past, maxi_is_zero, maxi_is_nega]
        count = 0
        for error in errors:
            count+=1
            if error is True:
                return render_template("welcome.html", club=found_club,
                                       competitions=competitions)

        return render_template("booking.html", club=found_club,
                               competition=found_competition,
                               maximum_booking=maximum_booking)
    else:
        return redirect(url_for("index"))


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    """Page sans template. Détermine si la réservation aboutit ou non."""
    places_form_empty = False
    places_form_negative = False
    places_form_err = False
    try:
        places_required = int(request.form["places"])
        if places_required < 0:
            places_form_negative = True
            flash(MESSAGE_INPUT_PLACES_NEGATIVE)
    except ValueError:
        if request.form["places"] == "":
            places_form_empty = True
            flash(MESSAGE_INPUT_PLACES_EMPTY)
        else:
            places_form_err = True
            flash(MESSAGE_ERROR_INPUT_PLACES)
        places_required = 0

    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

    comp_is_past = False
    zero_points_club = False
    nega_points_club = False
    zero_places_comp = False
    nega_places_comp = False
    over_12_required = False
    over_points_club = False
    over_places_comp = False
    over_12_with_old = False
    maxi_places_club = False
    nega_places_club = False
    if competition["date"] < today():
        comp_is_past = True
        flash(MESSAGE_ERROR_PAST_COMPETITION)
    if int(club["points"]) == 0:
        zero_points_club = True
        flash(MESSAGE_NOT_POINTS_CLUB)
    elif int(club["points"]) < 0:
        nega_points_club = True
        flash(MESSAGE_ERROR_DATA_CLUB_POINTS_NEGATIVE)
    if int(competition["number_of_places"]) == 0:
        zero_places_comp = True
        flash(MESSAGE_NOT_PLACES_COMP)
    elif int(competition["number_of_places"]) < 0:
        nega_places_comp = True
        flash(MESSAGE_ERROR_DATA_COMPETITION_PLACES_NEGATIVE)
    if places_required > 12:
        over_12_required = True
        flash(MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB)
    if places_required > int(club["points"]) // RATIO_POINTS_PLACE:
        over_points_club = True
        flash(MESSAGE_NOT_ENOUGH_POINTS)
    if places_required > int(competition["number_of_places"]):
        over_places_comp = True
        flash(MESSAGE_NOT_ENOUGH_PLACES)
    if club["name"] in competition["clubs_places"]:
        already_booked = int(competition["clubs_places"][club["name"]])
        if already_booked < 0:
            nega_places_club = True
            flash(MESSAGE_ERROR_DATA_CLUB_PLACES_NEGATIVE)
        elif already_booked == 12:
            maxi_places_club = True
            flash(MESSAGE_NOT_BOOKING_POSSIBLE)
        else:
            total_temp = already_booked + places_required
            if already_booked == 12 or total_temp > 12:
                over_12_with_old = True
                flash(MESSAGE_ERROR_OVER_12_PLACES_BY_CLUB)
    else:
        total_temp = places_required

    errors = [
        places_form_empty, places_form_negative, places_form_err, comp_is_past,
        zero_points_club, nega_points_club, zero_places_comp, nega_places_comp,
        over_12_required, over_points_club, over_places_comp, over_12_with_old,
        maxi_places_club, nega_places_club
    ]

    for error in errors:
        if error is True:
            return redirect(url_for("book",
                                    competition=request.form["competition"],
                                    club=request.form["club"]))

    competition["clubs_places"][club["name"]] = str(total_temp)
    club["points"] = str(int(club["points"])
                         - places_required * RATIO_POINTS_PLACE)
    competition["number_of_places"] = str(int(competition["number_of_places"])
                                          - places_required)
    update_database()
    flash(MESSAGE_GREAT_BOOKING)
    return redirect(url_for("show_summary"), code=307)


@app.route("/pointsBoard")
def points_board():
    """Page d'ensemble des clubs et de leur solde."""
    return render_template("points_board.html", clubs=load_clubs())


@app.route("/logout")
def logout():
    """Page de déconnexion. Page sans template."""
    return redirect(url_for("index"))
