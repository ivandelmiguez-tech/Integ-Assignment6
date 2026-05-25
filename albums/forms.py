from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from albums.models import Album, Photo

INPUT_CLASS = "form-input"


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = INPUT_CLASS
            if name == "username":
                field.widget.attrs["placeholder"] = "Choose a username"
                field.help_text = "Letters, numbers, and @/./+/-/_ only."
            elif name == "email":
                field.widget.attrs["placeholder"] = "you@example.com"
            elif "password" in name:
                field.widget.attrs["placeholder"] = "••••••••"


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("title", "description", "is_public")
        widgets = {
            "title": forms.TextInput(
                attrs={"class": INPUT_CLASS, "placeholder": "e.g. Summer 2026"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": INPUT_CLASS,
                    "rows": 4,
                    "placeholder": "What's this album about? (optional)",
                }
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
        }
        help_texts = {
            "is_public": "Anyone logged in can view public albums. Private albums are only visible to you and album admins.",
        }
        labels = {
            "is_public": "Make this album public",
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("image", "caption")
        widgets = {
            "image": forms.FileInput(attrs={"class": INPUT_CLASS, "accept": "image/*"}),
            "caption": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "Describe this photo (optional)",
                }
            ),
        }
        help_texts = {
            "image": "JPG, PNG, or GIF. Images are stored securely in the cloud.",
            "caption": "A short label helps you find photos later.",
        }
        labels = {
            "image": "Choose a photo",
        }
