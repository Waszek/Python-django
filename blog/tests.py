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

    def test_submit_form_creates_post(self):
        starting_post_count = Post.objects.count()

        form_data = {
            'title': 'Post send by automated test',
            'user_id': self.user.id
        }

        response = self.client.post(reverse('index'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), starting_post_count + 1)
        post_exists = Post.objects.filter(title='Post send by automated test').exists()
        self.assertTrue(post_exists)