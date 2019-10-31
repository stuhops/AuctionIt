
from django import forms
from .models import *
from stdimage import StdImageField, JPEGField
from phonenumber_field.modelfields import PhoneNumberField


class EditProfile(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.EmailField()
    # phone_number = PhoneNumberField(blank=False)
    # image = JPEGField(blank=False)


class EditProfilePost(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email')