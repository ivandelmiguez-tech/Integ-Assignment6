from django.contrib import admin

from albums.models import Album, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_public", "created_at")
    list_filter = ("is_public", "created_at")
    search_fields = ("title", "description", "owner__username")
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("album", "caption", "uploaded_at")
    list_filter = ("uploaded_at",)
