from booking.views import MAX_NUMBER_RESERVED_PLACES


class TestShowSummary:
    """Test the '/showSummary' endpoint."""

    def test_show_summary_with_known_email(self, client, load_clubs):
        """Test if the HTTP response code is 200 and the 'welcome' html page is
        displayed when the email address is known."""
        request_data = {"email": load_clubs[0]["email"]}
        response = client.post("/showSummary", data=request_data)
        data = response.data.decode()
        assert response.status_code == 200
        assert "Competitions" in data

    def test_show_summary_with_unknown_email(self, client, load_clubs):
        """Test if the HTTP response code is 404 and the error message is
        displayed when the email address is unknown."""
        request_data = {"email": load_clubs[0]["email"] + "x"}
        response = client.post("/showSummary", data=request_data)
        data = response.data.decode()
        assert response.status_code == 404
        assert "Oups" in data


class TestPurchasePlaces:
    """Test the '/purchasePlaces' endpoint."""

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
        response = client.post("/purchasePlaces", data=request_data)
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
        response = client.post("/purchasePlaces", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 403
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
        response = client.post("/purchasePlaces", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 403
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
        response = client.post("/purchasePlaces", data=request_data)
        response_data = response.data.decode()
        assert response.status_code == 403
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
        response = client.post("/purchasePlaces", data=request_data)
        points_after_purchase = int(load_clubs[0]["points"])
        assert response.status_code == 200
        assert points_after_purchase == points_before_purchase - int(places)


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
        """Test if the HTTP response code is 403 and and the error message is \
           displayed when the competition is not valid."""
        competition = load_competitions[0]["name"]
        club = load_clubs[0]["name"]
        response = client.get(f"/book/{competition}/{club}")
        response_data = response.data.decode()
        assert response.status_code == 403
        assert "has already taken place" in response_data
