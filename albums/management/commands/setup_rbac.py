from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from albums.models import Album, Photo


class Command(BaseCommand):
    help = "Create album_admin group and assign moderation permissions (RBAC)."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name=settings.ALBUM_ADMIN_GROUP)
        album_ct = ContentType.objects.get_for_model(Album)
        photo_ct = ContentType.objects.get_for_model(Photo)

        perms = Permission.objects.filter(
            content_type__in=[album_ct, photo_ct],
            codename__in=[
                "add_album",
                "change_album",
                "delete_album",
                "view_album",
                "add_photo",
                "change_photo",
                "delete_photo",
                "view_photo",
            ],
        )
        group.permissions.set(perms)

        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(f"{action} group '{settings.ALBUM_ADMIN_GROUP}' with {perms.count()} permissions.")
        )
        self.stdout.write("Assign users: python manage.py shell")
        self.stdout.write("  from django.contrib.auth.models import User, Group")
        self.stdout.write(f"  user = User.objects.get(username='your_admin')")
        self.stdout.write(f"  user.groups.add(Group.objects.get(name='{settings.ALBUM_ADMIN_GROUP}'))")
