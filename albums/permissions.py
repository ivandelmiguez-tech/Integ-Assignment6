from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin


def user_is_album_admin(user):
    """Album administrators belong to the album_admin group or are superusers."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=settings.ALBUM_ADMIN_GROUP).exists()


def user_can_manage_album(user, album):
    """Owners and album admins may edit or delete an album."""
    if not user.is_authenticated:
        return False
    if user_is_album_admin(user):
        return True
    return album.owner_id == user.pk


def user_can_view_album(user, album):
    """Public albums are visible to any logged-in user; private only to owner/admin."""
    if not user.is_authenticated:
        return False
    if user_is_album_admin(user) or album.owner_id == user.pk:
        return True
    return album.is_public


class AlbumAdminRequiredMixin(UserPassesTestMixin):
    """Restrict view to album administrators only."""

    def test_func(self):
        return user_is_album_admin(self.request.user)

    def handle_no_permission(self):
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, "Album administrator access is required.")
        return redirect("album_list")


class AlbumManagePermissionMixin(UserPassesTestMixin):
    """Allow album owner or album admin to perform the action."""

    def get_album(self):
        from albums.models import Album

        if getattr(self, "album", None):
            return self.album
        if getattr(self, "object", None):
            return self.object
        album_pk = self.kwargs.get("album_pk") or self.kwargs.get("pk")
        return Album.objects.get(pk=album_pk)

    def test_func(self):
        return user_can_manage_album(self.request.user, self.get_album())


class AlbumViewPermissionMixin(UserPassesTestMixin):
    """Allow viewing if user has permission on the album."""

    def test_func(self):
        return user_can_view_album(self.request.user, self.get_object())
