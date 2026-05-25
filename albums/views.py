from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from albums.forms import AlbumForm, PhotoForm, SignUpForm
from albums.models import Album, Photo
from albums.permissions import (
    AlbumAdminRequiredMixin,
    AlbumManagePermissionMixin,
    AlbumViewPermissionMixin,
    user_can_manage_album,
    user_is_album_admin,
)


class HomeView(TemplateView):
    template_name = "albums/home.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("album_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created. Welcome!")
        return response


class AlbumLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True


class AlbumLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = "albums/album_list.html"
    context_object_name = "albums"
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        qs = Album.objects.select_related("owner").prefetch_related("photos")
        if user_is_album_admin(user):
            return qs
        return qs.filter(Q(is_public=True) | Q(owner=user)).distinct()


class AlbumDetailView(LoginRequiredMixin, AlbumViewPermissionMixin, DetailView):
    model = Album
    template_name = "albums/album_detail.html"
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_manage"] = user_can_manage_album(self.request.user, self.object)
        context["photos"] = self.object.photos.all()
        return context


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = "albums/album_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Album created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("album_detail", kwargs={"pk": self.object.pk})


class AlbumUpdateView(LoginRequiredMixin, AlbumManagePermissionMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = "albums/album_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Album updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("album_detail", kwargs={"pk": self.object.pk})


class AlbumDeleteView(LoginRequiredMixin, AlbumManagePermissionMixin, DeleteView):
    model = Album
    template_name = "albums/album_confirm_delete.html"
    success_url = reverse_lazy("album_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Album deleted.")
        return super().delete(request, *args, **kwargs)


class PhotoCreateView(LoginRequiredMixin, AlbumManagePermissionMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = "albums/photo_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.album = Album.objects.get(pk=kwargs["album_pk"])
        return super().dispatch(request, *args, **kwargs)

    def get_album(self):
        return self.album

    def form_valid(self, form):
        form.instance.album = self.album
        messages.success(self.request, "Photo uploaded successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("album_detail", kwargs={"pk": self.album.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album"] = self.album
        return context


class PhotoManagePermissionMixin(UserPassesTestMixin):
    def get_photo(self):
        if getattr(self, "object", None):
            return self.object
        return Photo.objects.get(pk=self.kwargs["pk"])

    def get_album(self):
        return self.get_photo().album

    def test_func(self):
        return user_can_manage_album(self.request.user, self.get_album())


class PhotoUpdateView(LoginRequiredMixin, PhotoManagePermissionMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "albums/photo_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Photo updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("album_detail", kwargs={"pk": self.object.album_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album"] = self.object.album
        return context


class PhotoDeleteView(LoginRequiredMixin, PhotoManagePermissionMixin, DeleteView):
    model = Photo
    template_name = "albums/photo_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Photo deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("album_detail", kwargs={"pk": self.object.album_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album"] = self.object.album
        return context


class AdminDashboardView(LoginRequiredMixin, AlbumAdminRequiredMixin, ListView):
    """Album administrators see all albums for moderation."""

    model = Album
    template_name = "albums/admin_dashboard.html"
    context_object_name = "albums"
    paginate_by = 20

    def get_queryset(self):
        return Album.objects.select_related("owner").prefetch_related("photos")
