from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import MinValueValidator, MaxValueValidator
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
    rate = forms.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        widget=forms.NumberInput(attrs={'step': '0.1', 'min': '0.0', 'max': '5.0'})
    )

    class Meta:
        model = Review
        fields = ("rate", "text")
    