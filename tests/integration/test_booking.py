"""The integration tests for the booking app."""

from flask import url_for


def test_login_and_logout_are_successful(client, load_clubs):
    """Test to validate that a club can login and logout."""

    # Login a club with his email.
    login_data = {"email": load_clubs[0]["email"]}
    response = client.post("/showSummary", data=login_data)
    assert response.status_code == 200
    assert response.request.path == "/showSummary"

    # Logout redirect to the login page.
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == url_for("index")


def test_login_and_booking_access_are_successful(
    client, load_clubs, load_competitions
):
    """Test to validate that a club can login and access to the competition \
       booking page."""

    club = load_clubs[0]

    # Login a club with his email.
    login_data = {"email": club["email"]}
    response = client.post("/showSummary", data=login_data)
    assert response.status_code == 200
    response_data = response.data.decode()
    assert "Competitions" in response_data

    # Access the booking page of a competition.
    club_name = club["name"]
    competition_name = load_competitions[1]["name"]
    booking_url = f"/book/{competition_name}/{club_name}"
    response = client.get(booking_url)
    response_data = response.data.decode()
    assert response.status_code == 200
    assert "How many places ?" in response_data


def test_places_booking_is_successful(client, load_clubs, load_competitions):
    """Test to validate that a club can book places for a competition."""

    # Access the booking page of a competition.
    competition = load_competitions[1]["name"]
    club = load_clubs[0]["name"]
    booking_url = f"/book/{competition}/{club}"
    response = client.get(booking_url)
    response_data = response.data.decode()
    assert response.status_code == 200
    assert "How many places ?" in response_data

    # Book the places for this competition.
    request_data = {
        "club": club,
        "competition": competition,
        "places": "4",
    }
    response = client.post("/purchasePlaces", data=request_data)
    response_data = response.data.decode()
    assert response.status_code == 200
    assert response.request.path == "/purchasePlaces"
    assert "Great-booking complete !" in response_data
