from django.shortcuts import render
from django.contrib.auth import get_user_model

from posts.models import Post


User = get_user_model()


def home(request):
    posts = Post.objects.select_related(
        'author'
    ).prefetch_related(
        'media'
    ).all()

    return render(
        request,
        'core/home.html',
        {'posts': posts}
    )


def search(request):
    query = request.GET.get('q', '').strip()

    users = User.objects.none()

    if query:
        users = User.objects.filter(
            username__icontains=query,
            is_active=True
        ).order_by('username')[:30]

    return render(
        request,
        'core/search.html',
        {
            'query': query,
            'users': users
        }
    )
def explore(request):
    posts = Post.objects.filter(
        media__media_type='image'
    ).select_related(
        'author'
    ).prefetch_related(
        'media'
    ).distinct()

    return render(
        request,
        'core/explore.html',
        {
            'posts': posts
        }
    )