import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from model_bakery import baker
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def grouped_user():
    group = baker.make(Group, name="Marketers and Content Writers")
    user = baker.make(User)

    user.groups.add(group)

    return user
