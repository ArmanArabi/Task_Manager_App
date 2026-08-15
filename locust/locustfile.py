from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    
    # sont use @task -> so if set user number =10 , simulate 10 user not loot like task 
    def on_start(self): 
        response = self.client.post('/users/login', json={
            "username": "Mehrshad", 
            "password": "Mehrshad#123#" 
        })
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            self.client.headers = {'Authorization': f'Bearer {access_token}'}
        else:
            print("Login failed!")

    @task
    def hello_world(self):
        self.client.get("/")

    @task
    def not_found(self):
        self.client.get("/bye")

    @task
    def get_user(self):
        self.client.get("/tasks")