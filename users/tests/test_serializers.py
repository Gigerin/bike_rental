# tests/test_serializers.py
import pytest
from users.serializers import UserSerializer


@pytest.mark.django_db
def test_valid_user_serializer():
    valid_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "strongpassword123",
    }
    serializer = UserSerializer(data=valid_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == valid_data["email"]
    assert user.name == valid_data["name"]
    assert user.check_password(valid_data["password"])


@pytest.mark.django_db
def test_invalid_user_serializer():
    invalid_data = {"email": "gibberish", "name": "", "password": ""}
    serializer = UserSerializer(data=invalid_data)
    assert not serializer.is_valid()
    with pytest.raises(AssertionError):
        serializer.save()
