from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'biography',]

class UpdateMALUsernameForm(forms.Form):
    MAL_username = forms.CharField(
        label='MyAnimeList Username:',
        required=False,
    )

class UpdateAnimeForm(forms.Form):
        watched_anime_list = forms.CharField(
        label='Watched Anime:',
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False, 
    )