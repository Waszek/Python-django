from django.test import TestCase
from django.urls import reverse
from .models import BlogUser, Post

class BlogViewTests(TestCase):

    def setUp(self):
        self.user = BlogUser.objects.create(name="Tester Jan", company="CORPORATION")
        self.post = Post.objects.create(title="Test record", user=self.user)

    def test_blog_index_view_status_code(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

    def test_blog_index_view_displays_posts(self):
        response = self.client.get(reverse('index'))

        self.assertContains(response, "Test record")
        self.assertContains(response, "Tester Jan")