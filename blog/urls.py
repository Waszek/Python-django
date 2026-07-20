from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.api_post, name='api_post' ),
    path('drf/', views.drf_post_list, name='drf_post_list')
]