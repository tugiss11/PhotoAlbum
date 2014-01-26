from django import forms
from models import *

class AlbumOrderForm(forms.Form):
    client_name = forms.CharField(max_length = 256)
    client_address = forms.CharField(max_length = 256)
    client_email = forms.EmailField()