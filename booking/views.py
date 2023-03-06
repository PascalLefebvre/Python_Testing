import os
from datetime import datetime
import json

from flask import render_template, request, redirect, flash, url_for
from dotenv import load_dotenv

from booking import app


MAX_NUMBER_RESERVED_PLACES = 12

load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY", "something_special")


def load_clubs():
    with open("data/clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("data/competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


competitions = load_competitions()
clubs = load_clubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    """Display the competitions list."""
    try:
        club = [
            club for club in clubs if club["email"] == request.form["email"]
        ][0]
    except IndexError:
        flash(
            "Oups ! The email address is unknown. Please select a good one ..."
        )
        return render_template("messages.html"), 404
    else:
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """Select the competition for which a club whishes to book places."""
    try:
        found_club = [c for c in clubs if c["name"] == club][0]
        found_competition = [
            c for c in competitions if c["name"] == competition
        ][0]
    except IndexError:
        # Logout needed. Given the competition name and/or the club name are
        # unknown, the 'Book places' links will be wrong. Then, it must be
        # properly intialized by login again.
        flash("/!\\ Something went wrong ! You will be logout ...")
        return render_template("messages.html"), 404
    else:
        now = datetime.now()
        competition_date = datetime.strptime(
            found_competition["date"], "%Y-%m-%d %H:%M:%S"
        )
        if competition_date > now:
            return render_template(
                "booking.html", club=found_club, competition=found_competition
            )
        else:
            flash(
                f"/!\\ Sorry but the {found_competition['name']} competition \
                  has already taken place !"
            )
            return (
                render_template(
                    "welcome.html",
                    club=found_club,
                    competitions=competitions,
                ),
                400,
            )


@app.route("/purchase_places", methods=["POST"])
def purchase_places():
    """Book competition places."""
    HTTPResponseCode = 200
    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    try:
        places_required = int(request.form["places"])
    except ValueError:
        flash(
            f"/!\\ You have not indicated the number of places you wish to \
              book for the {competition['name']} competition !"
        )
        return (
            render_template(
                "welcome.html", club=club, competitions=competitions
            ),
            400,
        )

    if places_required > MAX_NUMBER_RESERVED_PLACES:
        flash(
            f"/!\\ Booking failure ! You are trying to book more than \
              {MAX_NUMBER_RESERVED_PLACES} places for a competition."
        )
        return (
            render_template(
                "welcome.html", club=club, competitions=competitions
            ),
            400,
        )

    if places_required <= int(club["points"]):
        if places_required <= int(competition["number_of_places"]):
            competition["number_of_places"] = (
                int(competition["number_of_places"]) - places_required
            )
            club["points"] = str(int(club["points"]) - places_required)
            flash(
                f"Great-booking complete ! You have booked {places_required}\
                  places for the {competition['name']} competition."
            )
        else:
            HTTPResponseCode = 400
            flash(
                f"/!\\ Booking failure ! You are trying to book more places \
                  than available for the {competition['name']} competition."
            )
    else:
        HTTPResponseCode = 400
        flash(
            f"/!\\ Booking failure ! You wish to book {places_required} \
              places but you have only {club['points']} points."
        )
    return (
        render_template("welcome.html", club=club, competitions=competitions),
        HTTPResponseCode,
    )


@app.route("/display_points")
def display_points():
    """Display club points."""
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M")
    sorted_clubs = sorted(clubs, key=lambda club: club["name"].lower())
    return render_template(
        "club_points.html", clubs=sorted_clubs, date=date, time=time
    )


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
