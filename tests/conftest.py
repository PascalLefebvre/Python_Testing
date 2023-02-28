import pytest

import booking.views
from booking import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture()
def load_clubs(monkeypatch):
    clubs = [
        {
            "name": "Titans",
            "email": "terry@incredible.millau.fr",
            "points": "5",
        },
    ]
    monkeypatch.setattr(booking.views, "clubs", clubs)
    return clubs


@pytest.fixture()
def load_competitions(monkeypatch):
    competitions = [
        {
            "name": "The French Statics Monsters",
            "date": "2022-10-30 09:00:00",
            "numberOfPlaces": "15",
        },
        {
            "name": "Bionic Brutes Of Strength",
            "date": "2023-03-12 09:00:00",
            "numberOfPlaces": "4",
        },
    ]
    monkeypatch.setattr(booking.views, "competitions", competitions)
    return competitions
