from django.shortcuts import render, redirect
from .models import Post, BlogUser

def index(request):
    #Create new post by user
    if request.method == 'POST':
        input_title = request.POST.get('title')
        input_user_id = request.POST.get('user_id')

        author = BlogUser.objects.get(id=input_user_id)

        Post.objects.create(title=input_title, user=author)

        return redirect('index')
  
    all_posts = Post.objects.all()
    all_users = BlogUser.objects.all()

    context = {
        'posts': all_posts,
        'users': all_users
    }
    return render(request, 'blog/index.html', context)