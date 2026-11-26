
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, ProfileEditForm
from posts.models import Post
from .models import Follow
User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Welcome to MarvelSpace! Your hero journey begins!'
            )

            return redirect('home')

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )



def profile(request, username):
    profile_user = get_object_or_404(
        User,
        username=username
    )

    posts = Post.objects.filter(
        author=profile_user
    ).prefetch_related('media')

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    is_following = False

    if request.user.is_authenticated:
        is_following = profile_user.followers.filter(
            follower=request.user
        ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'posts_count': posts.count(),
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }

    return render(
        request,
        'accounts/profile.html',
        context
    )

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your hero profile has been updated!'
            )

            return redirect(
                'profile',
                username=request.user.username
            )

    else:
        form = ProfileEditForm(instance=request.user)

    return render(
        request,
        'accounts/edit_profile.html',
        {'form': form}
    )

@login_required
def toggle_follow(request, username):
    if request.method != 'POST':
        return redirect('profile', username=username)

    profile_user = get_object_or_404(
        User,
        username=username
    )

    if request.user == profile_user:
        messages.error(
            request,
            "You cannot follow yourself!"
        )
        return redirect('profile', username=username)

    follow = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    )

    if follow.exists():
        follow.delete()

        messages.success(
            request,
            f"You unfollowed {profile_user.username}."
        )

    else:
        Follow.objects.create(
            follower=request.user,
            following=profile_user
        )

        messages.success(
            request,
            f"You are now following {profile_user.username}!"
        )

    return redirect('profile', username=username)
def followers_list(request, username):
    profile_user = get_object_or_404(
        User,
        username=username
    )

    follows = Follow.objects.filter(
        following=profile_user
    ).select_related('follower')

    return render(
        request,
        'accounts/followers.html',
        {
            'profile_user': profile_user,
            'follows': follows,
            'list_type': 'followers',
        }
    )


def following_list(request, username):
    profile_user = get_object_or_404(
        User,
        username=username
    )

    follows = Follow.objects.filter(
        follower=profile_user
    ).select_related('following')

    return render(
        request,
        'accounts/followers.html',
        {
            'profile_user': profile_user,
            'follows': follows,
            'list_type': 'following',
        }
    )