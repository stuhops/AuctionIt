
from django import forms
from .models import Profile


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email')
