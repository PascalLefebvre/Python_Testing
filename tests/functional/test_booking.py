"""The functional tests for the booking app."""
import time

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from booking import app


class TestLoginFailure(LiveServerTestCase):
    """Test the scenario that a club enters an unknown email."""

    def create_app(self):
        app.config.from_object("tests.config")
        return app

    def setUp(self):
        self.browser = webdriver.Firefox()

    def taerDown(self):
        self.browser.quit()

    def test_club_login_failure(self):
        self.browser.get(self.get_server_url())
        assert self.browser.current_url == "http://localhost:8943/"

        email_field = self.browser.find_element(By.NAME, "email")
        email_field.clear()
        email_field.send_keys("wrong@email.com")
        email_field.send_keys(Keys.RETURN)
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.ID, "follow"))
        )
        assert "The email address is unknown" in self.browser.page_source

        time.sleep(1)
        follow_link = self.browser.find_element(By.ID, "follow")
        follow_link.click()
        assert self.browser.current_url == "http://localhost:8943/"
