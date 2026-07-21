from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_post, name='api_post' ),
    path('drf/', views.drf_post_list, name='drf_post_list'),
    path('drf/<int:pk>', views.drf_post_detail, name='drf_post_detail'),
    path('cbv/posts', views.PostListAPIView.as_view(), name='cbv_post_list'),
    path('cbv/posts/<int:pk>', views.PostDetailsAPIView.as_view(), name='cbv_post_details'),
    path('cbv/generic/posts/<int:pk>', views.GenericPostDetailAPIView.as_view(), name='cbv_generic_post_details')
]