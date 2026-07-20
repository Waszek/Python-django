from django.db import models

#Table for users
class BlogUser(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Table for posts with foreign key
class Post(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)