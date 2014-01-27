from django import forms
from models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AlbumOrderForm(forms.Form):
    client_name = forms.CharField(max_length = 256)
    client_address = forms.CharField(max_length = 256)
    client_email = forms.EmailField()

