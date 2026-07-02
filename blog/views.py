from django.shortcuts import render
from .models import Post

def index(request):
    all_posts = Post.objects.all()
    context = {'posts': all_posts}
    return render(request, 'blog/index.html', context)