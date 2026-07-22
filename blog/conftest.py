import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from blog.models import BlogUser, Post

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_factory(db):
    def create_user(username="testuser", password="password123"):
        django_user = User.objects.create_user(username=username, password=password)
        blog_user, _ = BlogUser.objects.get_or_create(name=username)
        return django_user, blog_user
    return create_user

@pytest.fixture
def auth_client(api_client, user_factory):
    django_user, blog_user = user_factory()
    api_client.force_authenticate(user=django_user)
    return api_client, django_user, blog_user