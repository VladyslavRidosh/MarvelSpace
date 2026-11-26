
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Post, PostMedia, Like, Story
from datetime import timedelta
from django.utils import timezone


def validate_media(files, existing_media_count=0, existing_video=False):
    if not files:
        return True

    all_media_count = existing_media_count + len(files)

    if all_media_count > 3:
        return False

    has_video = existing_video

    for file in files:
        content_type = file.content_type

        if content_type.startswith('image/'):
            if has_video:
                return False

        elif content_type.startswith('video/'):
            if all_media_count != 1 or has_video:
                return False

            has_video = True

        else:
            return False

    return True


@login_required
def create_post(request):
    if request.user.role == 'civilian':
        messages.error(
            request,
            'You need to become a Hero to create posts!'
        )
        return redirect('home')

    if request.method == 'POST':
        post_form = PostForm(request.POST)
        files = request.FILES.getlist('files')

        if post_form.is_valid():
            if validate_media(files):
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()

                for file in files:
                    current_type = (
                        'video'
                        if file.content_type.startswith('video/')
                        else 'image'
                    )

                    PostMedia.objects.create(
                        post=post,
                        file=file,
                        media_type=current_type
                    )

                messages.success(
                    request,
                    'Your post has been published!'
                )
                return redirect('home')

            messages.error(
                request,
                'Invalid media selection. Use up to 3 photos or 1 video.'
            )
        else:
            messages.error(request, 'Please check the form.')

    else:
        post_form = PostForm()

    return render(
        request,
        'posts/create_post.html',
        {'post_form': post_form}
    )


@login_required
def edit_post(request, post_id):
    if request.user.role == 'civilian':
        messages.error(
            request,
            'You need to become a Hero to edit posts!'
        )
        return redirect('home')

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    existing_media = post.media.all()
    existing_media_count = existing_media.count()
    existing_video = existing_media.filter(
        media_type='video'
    ).exists()

    if request.method == 'POST':
        post_form = PostForm(
            request.POST,
            instance=post
        )

        files = request.FILES.getlist('files')

        if post_form.is_valid():
            if validate_media(
                files,
                existing_media_count,
                existing_video
            ):
                post_form.save()

                for file in files:
                    current_type = (
                        'video'
                        if file.content_type.startswith('video/')
                        else 'image'
                    )

                    PostMedia.objects.create(
                        post=post,
                        file=file,
                        media_type=current_type
                    )

                messages.success(
                    request,
                    'Your post has been updated!'
                )

                return redirect(
                    'profile',
                    username=request.user.username
                )

            messages.error(
                request,
                'Invalid media selection. Use up to 3 photos or 1 video.'
            )
        else:
            messages.error(request, 'Please check the form.')

    else:
        post_form = PostForm(instance=post)

    return render(
        request,
        'posts/edit_post.html',
        {
            'post_form': post_form,
            'post': post,
        }
    )


@login_required
@require_POST
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        return JsonResponse({
            'success': False,
            'error': 'You cannot like your own post.'
        }, status=400)

    like = Like.objects.filter(
        user=request.user,
        post=post
    ).first()

    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )
        liked = True

    return JsonResponse({
        'success': True,
        'liked': liked,
        'likes_count': post.likes.count()
    })
def stories(request):
    active_stories = Story.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).select_related(
        'author'
    ).order_by('-created_at')

    return render(
        request,
        'posts/stories.html',
        {
            'stories': active_stories
        }
    )

def story_viewer(request, story_id):
    active_stories = list(
        Story.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).select_related('author').order_by('-created_at')
    )

    story_index = next(
        (
            index
            for index, story in enumerate(active_stories)
            if story.id == story_id
        ),
        None
    )

    if story_index is None:
        return redirect('stories')

    story = active_stories[story_index]

    previous_story = (
        active_stories[story_index - 1]
        if story_index > 0
        else None
    )

    next_story = (
        active_stories[story_index + 1]
        if story_index < len(active_stories) - 1
        else None
    )

    expires_at = story.created_at + timedelta(hours=24)
    remaining_time = expires_at - timezone.now()

    return render(
        request,
        'posts/story_viewer.html',
        {
            'story': story,
            'previous_story': previous_story,
            'next_story': next_story,
            'remaining_seconds': max(
                0,
                int(remaining_time.total_seconds())
            ),
        }
    )

@login_required
def create_story(request):
    if request.user.role != 'avenger':
        messages.error(
            request,
            'Only Avengers can publish stories!'
        )
        return redirect('stories')

    if request.method == 'POST':
        file = request.FILES.get('file')

        if not file:
            messages.error(request, 'Please select a file.')
            return redirect('create_story')

        content_type = file.content_type

        if content_type.startswith('image/'):
            media_type = 'image'
        elif content_type.startswith('video/'):
            media_type = 'video'
        else:
            messages.error(
                request,
                'Only images and videos are allowed.'
            )
            return redirect('create_story')

        Story.objects.create(
            author=request.user,
            file=file,
            media_type=media_type
        )

        messages.success(
            request,
            'Your story has been published!'
        )
        return redirect('stories')

    return render(request, 'posts/create_story.html')
@login_required
@require_POST
def delete_story(request, story_id):
    story = get_object_or_404(
        Story,
        id=story_id,
        author=request.user
    )

    story.file.delete(save=False)
    story.delete()

    messages.success(request, 'Your story has been deleted!')

    return redirect('stories')