from locust import HttpUser, task



class WebsiteUser(HttpUser):
    @task
    def view_apartments(self):
        self.client