from django import forms
from accounts.models import Profile
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class registerform(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
