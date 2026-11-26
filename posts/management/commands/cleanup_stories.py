
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from posts.models import Story


class Command(BaseCommand):
    help = 'Delete stories older than 24 hours'

    def handle(self, *args, **options):
        expiration_time = timezone.now() - timedelta(hours=24)

        expired_stories = Story.objects.filter(
            created_at__lt=expiration_time
        )

        deleted_count = 0

        for story in expired_stories:
            story.file.delete(save=False)
            story.delete()
            deleted_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Deleted {deleted_count} expired stories.'
            )
        )
