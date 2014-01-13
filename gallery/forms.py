from django.forms import ModelForm
from models import *

class ImageURLForm(ModelForm):
    class Meta:
        model = AlbumImage
        fields = ["url"]