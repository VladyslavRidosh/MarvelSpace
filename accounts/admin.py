
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'xp',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
    )

    search_fields = (
        'username',
        'email',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('MarvelSpace Profile', {
            'fields': (
                'avatar',
                'bio',
                'role',
                'xp',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('MarvelSpace Profile', {
            'fields': (
                'email',
                'avatar',
                'bio',
                'role',
                'xp',
            )
        }),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):

    list_display = (
        'follower',
        'following',
        'created_at',
    )

    search_fields = (
        'follower__username',
        'following__username',
    )

    list_filter = (
        'created_at',
    )
