# tests/test_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_registration_view():
    client = APIClient()
    url = reverse("register")
    data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "strongpassword123",
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(email=data["email"])
    assert user.name == data["name"]
    assert user.check_password(data["password"])


@pytest.mark.django_db
def test_user_registration_invalid_data():
    client = APIClient()
    url = reverse("register")
    data = {"email": "not-an-email", "name": "", "password": ""}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
