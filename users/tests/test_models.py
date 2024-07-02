# tests/test_models.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email='test@example.com', name='Test User', password='strongpassword123')
    assert user.email == 'test@example.com'
    assert user.name == 'Test User'
    assert user.check_password('strongpassword123')
    assert user.is_active
    assert not user.is_admin

@pytest.mark.django_db
def test_create_superuser():
    admin_user = User.objects.create_superuser(email='admin@example.com', name='Admin User', password='strongpassword123')
    assert admin_user.email == 'admin@example.com'
    assert admin_user.name == 'Admin User'
    assert admin_user.check_password('strongpassword123')
    assert admin_user.is_active
    assert admin_user.is_admin
