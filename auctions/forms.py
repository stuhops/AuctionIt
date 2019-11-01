
from django import forms
from .models import Profile


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        # TODO: The image item does not upload
        fields = ('name', 'email', 'phone_number', 'image')
