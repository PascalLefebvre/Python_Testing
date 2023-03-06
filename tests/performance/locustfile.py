from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task(2)
    def list_competitions(self):
        self.client.post("/show_summary", {"email": "kate@shelifts.co.uk"})

    @task
    def display_club_points(self):
        self.client.get("/display_points")
