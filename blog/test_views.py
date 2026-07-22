import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Post

@pytest.mark.django_db
def test_get_posts_list():
    client = APIClient()
    url = reverse('post-list')

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_anonymous_user_POST(api_client):
    url = reverse('post-list')

    response = api_client.post(url)

    assert response.status_code == 403

@pytest.mark.django_db
def test_logged_user_POST(auth_client):
    api_client, django_user, blog_user = auth_client

    payload = {'title': "Simple title"}


    url = reverse('post-list')
    response = api_client.post(url, data=payload)

    post_count = Post.objects.count()
    created_post= Post.objects.first()

    assert response.status_code == 201
    assert post_count == 1
    assert created_post.user == blog_user    


@pytest.mark.django_db
def test_user_cannot_update_other_user_post(auth_client, user_factory):
    api_client, django_user, blog_user = auth_client
    django_second_user, blog_second_user = user_factory(username='John')

    payload = {
        'title': 'My title',
    }

    post = Post.objects.create(**payload, user=blog_second_user)
    url = reverse('post-detail', kwargs={'pk': post.pk})

    new_payload = {
        'title': 'My title 2'
    }
    
    response = api_client.put(url, new_payload)

    assert response.status_code == 403