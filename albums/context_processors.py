from albums.permissions import user_is_album_admin


def rbac(request):
    return {
        "is_album_admin": user_is_album_admin(request.user) if request.user.is_authenticated else False,
    }
