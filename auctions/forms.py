
from django import forms
from .models import Profile
from stdimage import StdImageField, JPEGField
from phonenumber_field.modelfields import PhoneNumberField


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email')