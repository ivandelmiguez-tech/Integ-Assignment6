from django.urls import path

from albums import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("albums/", views.AlbumListView.as_view(), name="album_list"),
    path("albums/create/", views.AlbumCreateView.as_view(), name="album_create"),
    path("albums/<int:pk>/", views.AlbumDetailView.as_view(), name="album_detail"),
    path("albums/<int:pk>/edit/", views.AlbumUpdateView.as_view(), name="album_update"),
    path("albums/<int:pk>/delete/", views.AlbumDeleteView.as_view(), name="album_delete"),
    path(
        "albums/<int:album_pk>/photos/add/",
        views.PhotoCreateView.as_view(),
        name="photo_create",
    ),
    path("photos/<int:pk>/edit/", views.PhotoUpdateView.as_view(), name="photo_update"),
    path("photos/<int:pk>/delete/", views.PhotoDeleteView.as_view(), name="photo_delete"),
    path("admin-dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/login/", views.AlbumLoginView.as_view(), name="login"),
    path("accounts/logout/", views.AlbumLogoutView.as_view(), name="logout"),
]
