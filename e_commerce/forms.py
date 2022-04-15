from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
  
    class Meta:
        model = Profile
        fields = ['country', 'state', 'city', 'postal_code', 'cell_phone_number', 'avatar']     
