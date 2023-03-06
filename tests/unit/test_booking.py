"""The unit tests for the booking app."""

import re

from booking.views import MAX_NUMBER_RESERVED_PLACES


class TestShowSummary:
    """Test the '/show_summary' endpoint."""

    def test_show_summary_with_known_email_status_code_ok(
        self, client, load_clubs
    ):
        """Test if the HTTP response code is 200."""
        request_data = {"email": load_clubs[0]["email"]}
        response = client.post("/show_summary", data=request_data)
        assert response.status_code == 200

    def test_show_summary_with_known_email_book_places_link_valid(
        self, client, load_clubs, load_competitions
    ):
        """Test if the link to book places for the first displayed \
           competition is valid."""
        club_name = load_clubs[0]["name"]
        competition_name = load_competitions[0]["name"]
        book_places_link = "/book" + "/" + competition_name + "/" + club_name
        # The space character is replaced by the hexa code '%20' in the URL.
        book_places_link = book_places_link.replace(" ", "%20")
        request_data = {"email": load_clubs[0]["email"]}
        response = client.post("/show_summary", data=request_data)
        data = response.data.decode()
        assert book_places_link in data

    def test_show_summary_with_unknown_email(self, client, load_clubs):
        """Test if the HTTP response code is 404 and the error message is
        displayed when the email address is unknown."""
        request_data = {"email": load_clubs[0]["email"] + "x"}
        response = client.post("/show_summary", data=request_data)
        data = response.data.decode()
        assert response.status_code == 404
        assert "The email address is unknown" in data


class TestPurchasePlaces:
    """Test the '/purchase_places' endpoint."""

    def test_purchase_places_with_enough_points(
        self, client, load_clubs, load_competitions
    ):
        """Test if the confirmation message is displayed when a club has
        enough points to book competition places."""
        request_data = {
            "club": load_clubs[0]["name"],
            "competition": load_competitions[0]["name"],
            "places": "4",
        }
        response = client.post("/purchase_places", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 200
        assert "Great-booking complete !" in response_data

    def test_purchase_places_without_enough_points(
        self, client, load_clubs, load_competitions
    ):
        """Test if the failure message is displayed when a club hasn't enough
        points to book competition places."""
        request_data = {
            "club": load_clubs[0]["name"],
            "competition": load_competitions[0]["name"],
            "places": "6",
        }
        response = client.post("/purchase_places", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 400
        assert "but you have only" in response_data

    def test_purchase_more_places_than_available(
        self, client, load_clubs, load_competitions
    ):
        """Test if the failure message is displayed when a club is trying to
        book more places than available for the competition."""
        request_data = {
            "club": load_clubs[0]["name"],
            "competition": load_competitions[1]["name"],
            "places": "5",
        }
        response = client.post("/purchase_places", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 400
        assert "to book more places" in response_data

    def test_purchase_more_places_than_12_places(
        self, client, load_clubs, load_competitions
    ):
        """Test if the failure message is displayed when a club is trying to
        book more than 12 places for a competition."""
        places = str(MAX_NUMBER_RESERVED_PLACES + 1)
        request_data = {
            "club": load_clubs[0]["name"],
            "competition": load_competitions[0]["name"],
            "places": places,
        }
        response = client.post("/purchase_places", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 400
        assert f"{MAX_NUMBER_RESERVED_PLACES} places" in response_data

    def test_update_points_if_purchased_places(
        self, client, load_clubs, load_competitions
    ):
        """When a club secretary redeems points for places in a competition,
        test if the amount of points used is deducted from the club's balance.
        """
        points_before_purchase = int(load_clubs[0]["points"])
        places = "4"
        request_data = {
            "club": load_clubs[0]["name"],
            "competition": load_competitions[0]["name"],
            "places": places,
        }
        response = client.post("/purchase_places", data=request_data)
        points_after_purchase = int(load_clubs[0]["points"])
        assert response.status_code == 200
        assert points_after_purchase == points_before_purchase - int(places)

    def test_purchase_places_if_places_field_is_empty(
        self, client, load_clubs, load_competitions
    ):
        """Test if the HTTP response code is 400 and and the error message is \
           displayed when the places field is not filled."""
        request_data = {
            "club": load_clubs[0]["name"],
            "competition": load_competitions[0]["name"],
            "places": "",
        }
        response = client.post("/purchase_places", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 400
        assert "You have not indicated the number of places" in response_data


class TestBookPlaces:
    """Test the '/book/<competition>/<club>' endpoint."""

    def test_book_places_with_wrong_club_name_in_url(
        self, client, load_clubs, load_competitions
    ):
        """Test if the HTTP response code is 404 and the error message is \
           displayed when the club name in the url is wrong."""
        competition = load_competitions[0]["name"]
        club = load_clubs[0]["name"] + "x"
        response = client.get(f"/book/{competition}/{club}")
        response_data = response.data.decode()
        assert response.status_code == 404
        assert "Something went wrong !" in response_data

    def test_book_places_in_future_competition(
        self, client, load_clubs, load_competitions
    ):
        """Test if the HTTP response code is 200 and and the 'booking' html
        page is displayed when the competition is valid."""
        competition = load_competitions[1]["name"]
        club = load_clubs[0]["name"]
        response = client.get(f"/book/{competition}/{club}")
        response_data = response.data.decode()
        assert response.status_code == 200
        assert "How many places ?" in response_data

    def test_book_places_in_past_competition(
        self, client, load_clubs, load_competitions
    ):
        """Test if the HTTP response code is 400 and and the error message is \
           displayed when the competition is not valid."""
        competition = load_competitions[0]["name"]
        club = load_clubs[0]["name"]
        response = client.get(f"/book/{competition}/{club}")
        response_data = response.data.decode()
        assert response.status_code == 400
        assert "has already taken place" in response_data


class TestDisplayPoints:
    """Test the '/display_points' endpoint."""

    def test_display_points_status_code_ok(self, client):
        """Test if the HTTP response code is 200."""
        response = client.get("/display_points")
        assert response.status_code == 200

    def test_display_points_number_rows_of_scoreboard_ok(
        self, client, load_clubs
    ):
        """Test if the numbers of rows of the score table (included the \
           headers line) is ok."""
        number_of_clubs = len(load_clubs)
        response = client.get("/display_points")
        data = response.data.decode()
        # Count the number of HTML table row tags in the page content.
        pattern_string = re.compile("<tr>")
        number_of_lines = len(pattern_string.findall(data))
        # '+1' corresponds to the headers line.
        assert number_of_lines == (number_of_clubs + 1)

    def test_display_points_scoreboard_fields_ok(self, client, load_clubs):
        """Test if the score table contains the name of the club and its \
           number of points."""
        club_name = load_clubs[0]["name"]
        club_points = load_clubs[0]["points"]
        response = client.get("/display_points")
        data = response.data.decode()
        assert club_name in data
        assert club_points in data
