from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class UserRegisterForm(UserCreationForm):
    # User =
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'classes','sekolah','email', 'password1', 'password2']

class UserCreationForm(UserCreationForm):
    # User = get_user_model()
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username',)


class UserChangeForm(UserChangeForm):
    # User = get_user_model()
    class meta:
        model = get_user_model()
        fields = ('email', 'username')

