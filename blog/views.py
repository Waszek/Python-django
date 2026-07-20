from django.shortcuts import render, redirect
from .models import Post, BlogUser
from django.http import JsonResponse, HttpResponseNotAllowed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework import status

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

# convert data to JSON manually
def api_post(request):

    if request.method != "GET":
       return HttpResponseNotAllowed(['GET'])
    
    all_posts = Post.objects.all()

    posts_list =[]
    for post in all_posts:
        posts_list.append({
            'title': post.title,
            'author': post.user.name,
            'company': post.user.company
        })

    data = {
        'posts': posts_list
    }
       
    return JsonResponse(data)
    
# convert data to JSON by DRF serializer
@api_view(['GET', 'POST'])
def drf_post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            first_name = BlogUser.objects.first()
            serializer.save(user=first_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)