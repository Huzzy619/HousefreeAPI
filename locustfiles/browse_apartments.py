from locust import HttpUser, task, between
import random
import json
from django.contrib.auth import get_user_model
import django

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # @task
    def view_apartments(self):
        self.client.get('/apartment/', name = '/apartment/')
        print(self.result)


    # @task
    def view_apartment(self):
        apartment_id = random.randint(1,4)
        self.client.get(f'/apartment/{apartment_id}', name = '/apartment/:id/')
    
    @task
    def create_apartments(self):
        django.setup()
        self.client.post('/apartment/', name = '/apartment/create', json={
            
        "title": "string",
        "category": "Bungalow",
        "price": random.randint(1000, 3000),
        "location": "string",
        "specifications": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
        },
        "descriptions": "string",
        "is_available": True,
         "agent": "25c4c886-77b6-49bf-b9e3-f6e9fd263819"

        })


    def make_booking(self):
        self.client.post('/bookmark/', json={

        })
    
    # def on_start(self):
    #     response = self.client.post('/accounts/login/', json={
    #         "email": "school@django.com",
    #         "password": "@Huzkid619",
    #         # "password2": "@Huzkid619",
    #         # "first_name": "string",
    #         # "last_name": "string",
    #         # "is_agent": True
    #     })
    #     self.result = response.json()
    #     # for _ in range(10):
    #     #     print(result)
    #     # self.user_id = result["user"]["pk"]
    #     # print(self.user_id)
