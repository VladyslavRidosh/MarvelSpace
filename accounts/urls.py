
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path(
        'profile/<str:username>/follow/',
        views.toggle_follow,
        name='toggle_follow'
    ),

    path(
        'profile/<str:username>/followers/',
        views.followers_list,
        name='followers_list'
    ),

    path(
        'profile/<str:username>/following/',
        views.following_list,
        name='following_list'
    ),

    path('profile/<str:username>/', views.profile, name='profile'),
]
