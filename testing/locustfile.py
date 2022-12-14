from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        # Main Pages
        self.client.get("/")
        self.client.get("/home")
        self.client.get("/members")
        self.client.get("/profile")
        self.client.get("/myprofile")
        self.client.get("/announcements")
        self.client.get("/form")
        self.client.get("/upload_post_image_page")
        self.client.get("/admin")
        self.client.get("/donations")