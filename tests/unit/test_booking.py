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
        assert "You don&#39;t have enough points !" in response_data
