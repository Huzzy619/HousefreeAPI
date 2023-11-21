import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status

from blog.models import Blog

User = get_user_model()
blog_data = {
    "title": "string",
    "content": "string",
    "category": "Spotlight",
    "featured": True,
}


@pytest.mark.django_db
class TestBlog:
    def test_getting_all_blogs_returns_200(self, api_client):

        response = api_client.get("/blogs/")

        assert response.status_code == status.HTTP_200_OK

    def test_getting_blog_detail_returns_200(self, api_client):

        blog = baker.make(Blog)

        response = api_client.get(f"/blogs/{blog.id}/")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCreateBlog:
    def test_blog_creation_by_group_member_returns_201(self, api_client, grouped_user):

        api_client.force_authenticate(user=grouped_user)

        response = api_client.post("/blogs/", blog_data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED

    def test_blog_creation_by_superuser_returns_201(self, api_client):

        user = baker.make(User, is_superuser=True)

        api_client.force_authenticate(user=user)

        response = api_client.post(
            "/blogs/",
            blog_data,
            format="multipart",
        )

        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestUpdateBlog:
    def test_update_blog_returns_200(self, api_client, grouped_user):

        blog = baker.make(Blog)

        api_client.force_authenticate(user=grouped_user)
        response = api_client.patch(f"/blogs/{blog.id}/", blog_data)

        assert response.status_code == status.HTTP_200_OK

    def test_is_user_is_anonymous_returns_401(self, api_client, grouped_user):

        blog = baker.make(Blog)

        response = api_client.patch(f"/blogs/{blog.id}/", blog_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestDeleteBlog:
    def test_deleting_blog_by_group_member_returns_204(self, api_client, grouped_user):

        blog = baker.make(Blog)

        api_client.force_authenticate(user=grouped_user)
        response = api_client.delete(f"/blogs/{blog.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT


    def test_deleting_blog_by_superuser_returns_204(self, api_client):

        blog = baker.make(Blog)
        user = baker.make(User, is_superuser=True)

        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/blogs/{blog.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT


    def test_is_user_is_anonymous_returns_401(self, api_client):

        blog = baker.make(Blog)

        response = api_client.delete(f"/blogs/{blog.id}/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
