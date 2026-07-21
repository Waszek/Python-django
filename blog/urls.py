from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts-set', views.PostViewSet, basename='post')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_post, name='api_post' ),
    path('drf/', views.drf_post_list, name='drf_post_list'),
    path('drf/<int:pk>', views.drf_post_detail, name='drf_post_detail'),
    path('cbv/posts', views.PostListAPIView.as_view(), name='cbv_post_list'),
    path('cbv/posts/<int:pk>', views.PostDetailsAPIView.as_view(), name='cbv_post_details'),
    path('cbv/generic/posts/<int:pk>', views.GenericPostDetailAPIView.as_view(), name='cbv_generic_post_details'),
    path('api-auth/', include('rest_framework.urls')),
] + router.urls