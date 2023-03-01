import os
from datetime import datetime
import json

from flask import render_template, request, redirect, flash, url_for
from dotenv import load_dotenv

from booking import app


MAX_NUMBER_RESERVED_PLACES = 12

load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY", "something_special")


def loadClubs():
    with open("data/clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("data/competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
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
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [
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
            foundCompetition["date"], "%Y-%m-%d %H:%M:%S"
        )
        if competition_date > now:
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition
            )
        else:
            flash(
                f"/!\\ Sorry but the {foundCompetition['name']} competition \
                  has already taken place !"
            )
            return (
                render_template(
                    "welcome.html",
                    club=foundClub,
                    competitions=competitions,
                ),
                403,
            )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    http_response_code = 200
    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])

    if placesRequired > MAX_NUMBER_RESERVED_PLACES:
        http_response_code = 403
        flash(
            f"/!\\ Booking failure ! You are trying to book more than \
              {MAX_NUMBER_RESERVED_PLACES} places for a competition."
        )
        return (
            render_template(
                "welcome.html", club=club, competitions=competitions
            ),
            http_response_code,
        )

    if placesRequired <= int(club["points"]):
        if placesRequired <= int(competition["numberOfPlaces"]):
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = str(int(club["points"]) - placesRequired)
            flash(
                f"Great-booking complete ! You booked {placesRequired} places \
                  for the {competition['name']} competition."
            )
        else:
            http_response_code = 403
            flash(
                f"/!\\ Booking failure ! You are trying to book more places \
                  than available for the {competition['name']} competition."
            )
    else:
        http_response_code = 403
        flash(
            f"/!\\ Booking failure ! You want to book {placesRequired} places \
              but you have only {club['points']} points."
        )
    return (
        render_template("welcome.html", club=club, competitions=competitions),
        http_response_code,
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
