
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),

    path('stories/', views.stories, name='stories'),
    path('stories/create/', views.create_story, name='create_story'),
    path('stories/<int:story_id>/delete/',views.delete_story,name='delete_story'),
    path('stories/<int:story_id>/',views.story_viewer,name='story_viewer'),
]