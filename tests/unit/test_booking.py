from booking.views import MAX_NUMBER_RESERVED_PLACES


class TestShowSummary:
    """Test the '/showSummary' endpoint."""

    def test_show_summary_with_known_email_status_code_ok(
        self, client, load_clubs
    ):
        # Set up data or the environment (Given/Arrange)
        request_data = {"email": load_clubs[0]["email"]}
        # Some action is performed (When/Act)
        response = client.post("/showSummary", data=request_data)
        # Some expected result or end state should happen (Then/Assert)
        assert response.status_code == 200

    def test_show_summary_with_known_email_display_word_competitions(
        self, client, load_clubs
    ):
        """Test if the 'welcome' html page is displayed when the email address
        is known."""
        request_data = {"email": load_clubs[0]["email"]}
        response = client.post("/showSummary", data=request_data)
        data = response.data.decode()
        assert "Competitions" in data

    def test_show_summary_with_unknown_email_display_word_oups(
        self, client, load_clubs
    ):
        """Test if the 'unknown_email' html page is displayed when the email
        address is unknown."""
        request_data = {"email": load_clubs[0]["email"] + "bad"}
        response = client.post("/showSummary", data=request_data)
        data = response.data.decode()
        assert "Oups" in data

    def test_show_summary_with_unknown_email_status_code_404(
        self, client, load_clubs
    ):
        request_data = {"email": load_clubs[0]["email"] + "bad"}
        response = client.post("/showSummary", data=request_data)
        assert response.status_code == 404


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
        # response_data = response.data.decode()
        points_after_purchase = int(load_clubs[0]["points"])
        assert response.status_code == 200
        assert points_after_purchase == points_before_purchase - int(places)
