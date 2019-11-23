
from django import forms
from .models import Profile


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email', 'phone_number', 'image', 'auctions')


# class JoinAuction(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('auctions',)
