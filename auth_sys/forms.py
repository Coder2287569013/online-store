from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Review

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "avatar")

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser 
        fields = ("username", "email", "first_name", "last_name", "avatar")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rate", "text")
    