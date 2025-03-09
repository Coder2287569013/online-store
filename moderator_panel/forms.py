from django import forms
from .models import ChangeRequest

class ChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ChangeRequest
        fields = ('message',)