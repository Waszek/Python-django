from .models import Post, BlogUser
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from .serializers import PostSerializer

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


@api_view(['GET', 'PUT', 'DELETE'])
def drf_post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#converted data by APIView class
class PostListAPIView(APIView):
    def get_serializer(self, *args, **kwargs):
        return PostSerializer(*args, **kwargs)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            first_name = BlogUser.objects.first()
            serializer.save(user=first_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostDetailsAPIView(APIView):
    def get_serializer(self, *args, **kwargs):
        return PostSerializer(*args, **kwargs)
    
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#converted data by generics
class GenericPostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#converted data by viewSets
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        user = BlogUser.objects.first()
        serializer.save(user=user)