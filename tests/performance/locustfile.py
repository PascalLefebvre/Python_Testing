from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def list_competitions(self):
        self.client.post("/showSummary", {"email": "kate@shelifts.co.uk"})
