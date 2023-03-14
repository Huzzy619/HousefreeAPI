# (Arrange, Act, Assert) - AAA


import random

import pytest
from model_bakery import baker
from rest_framework import status

from apartments.models import Apartment
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestApartmentCreation:

    apartment_data = {
        "title": "string",
        "category": "Apartments",
        "_type": "Rent",
        "price": 99999999,
        "address": "string",
        "state": "string",
        "map_link": "https://localhost:8000",
        "specifications": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string",
        },
        "descriptions": "string",
        "is_available": True,
    }

    def test_if_user_is_not_agent_returns_403(self, api_client, authenticate):

        authenticate()
        response = api_client.post(
            "/apartment/",
            self.apartment_data,
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_agent_returns_201(self, api_client, authenticate):

        authenticate(is_agent=True)

        response = api_client.post(
            "/apartment/",
            self.apartment_data,
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestApartmentSearch:
    def test_if_users_can_search_apartments_returns_200(self, api_client, authenticate):

        authenticate()

        response = api_client.get("/apartment/")

        assert response.status_code == status.HTTP_200_OK

    def test_viewing_an_apartment_detail_returns_200(self, api_client, authenticate):
        apartment = baker.make(Apartment)
        authenticate()

        response = api_client.get(f"/apartment/{apartment.id}/")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestApartmentBookmark:
    def test_viewing_bookmarked_apartments_by_anonymous_user_returns_401(
        self, api_client
    ):

        response = api_client.get("/bookmark/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_viewing_bookmarked_apartments_by_authenticated_user_returns_200(
        self, api_client, authenticate
    ):

        authenticate()

        response = api_client.get("/bookmark/")

        assert response.status_code == status.HTTP_200_OK

    def test_bookmarking_apartment_returns_200(self, api_client, authenticate):
        authenticate()
        apartment = baker.make(Apartment)

        response = api_client.post("/bookmark/", {"apartment_id": apartment.id})

        assert response.status_code == status.HTTP_201_CREATED

    def test_deleting_bookmark_returns_204(self, api_client, authenticate):
        authenticate()
        apartments = baker.make(Apartment, random.randint(1, 10))

        _ids = [apartment.id for apartment in apartments]
        response = api_client.delete("/bookmark/", data={"items": _ids}, format="json")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_deleting_bookmark_by_anonymous_user_returns_401(self, api_client):
        apartments = baker.make(Apartment, random.randint(1, 10))

        _ids = [apartment.id for apartment in apartments]
        response = api_client.delete("/bookmark/", data={"items": _ids}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestApartmentDeletion:

    def test_delete_apartment_returns_204(self, api_client):
        user = baker.make(User, is_agent=True)
        apartment = baker.make(Apartment, agent = user)

        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/apartment/{apartment.id}/")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_apartment_owned_by_another_agent_returns_403(self, api_client):
        user1 = baker.make(User, is_agent=True)

        apartment = baker.make(Apartment, agent = user1)

        user2 = baker.make(User, is_agent=True)
        api_client.force_authenticate(user=user2)


        response = api_client.delete(f"/apartment/{apartment.id}/")
        
        assert response.status_code != status.HTTP_403_FORBIDDEN
