from django.db import models
from django.contrib.auth.models import User
from layouts.layout_info import PAGE_LAYOUTS, NAME_DB_MAX_LENGTH

import uuid

def createAlbum(title, owner = None):
    album = Album(title = title, owner = owner)
    album.save()
    return album

class Album(models.Model):
    title = models.CharField(max_length = 256)
    owner = models.ForeignKey(User, blank = True, related_name = "Albums") 
    album_id = models.CharField(max_length = 36, unique = True, default=lambda:str(uuid.uuid4()))
    public = models.BooleanField(default = False)

    def addPage(self, layout = "default"):
        page = AlbumPage(album = self, layout = layout, idx = len(self.pages.all()) + 1)
        page.save()
        for i in xrange(10): # TODO: maybe this should be done better?
            page.addImage()
        page.save()

        return page # Maybe someone is interested in this

    def fixPageNumbers(self):
        i = 1
        for page in self.pages.all().order_by("idx"):
            page.idx = i
            i += 1
            page.save()

    def delete(self, *args, **kwargs):
        AlbumPage.objects.filter(album = self).delete()
        super(Album, self).delete(*args, **kwargs)

class AlbumPage(models.Model):
    idx = models.IntegerField()
    album = models.ForeignKey(Album, related_name = "pages")
    layout = models.CharField(max_length = NAME_DB_MAX_LENGTH, choices = PAGE_LAYOUTS, default = PAGE_LAYOUTS[0])
    page_id = models.CharField(max_length = 36, unique = True, default=lambda:str(uuid.uuid4()))

    def addImage(self):
        image = AlbumImage(page = self, idx = len(self.images.all()))
        image.save()

        return image # Maybe someone is interested in this

    def delete(self, *args, **kwargs):
        AlbumPage.objects.filter(page = self).delete()
        super(AlbumPage, self).delete(*args, **kwargs)

    class Meta:
        ordering = ["idx"]

class AlbumImage(models.Model):
    idx = models.IntegerField()
    page = models.ForeignKey(AlbumPage, related_name = "images")
    url = models.URLField(max_length = 1000, default = "")
    caption = models.TextField(default = "")
    image_id = models.CharField(max_length = 36, unique = True, default=lambda:str(uuid.uuid4()))

    class Meta:
        ordering = ["idx"]

class AlbumOrder(models.Model):
    # DB details
    order_id = models.CharField(max_length = 36, unique = True, default=lambda:str(uuid.uuid4()))
    owner = models.ForeignKey(User, related_name = "+")
    album = models.ForeignKey(Album, related_name='+')
    
    # Payment details
    price = models.DecimalField(decimal_places = 2, max_digits = 6)
    payment_succesful = models.BooleanField(default = False)
    payment_reference_number = models.CharField(max_length = 256)

    # Order details
    date = models.DateTimeField(auto_now_add = True)
    client_name = models.CharField(max_length = 256)
    client_address = models.CharField(max_length = 256)
    client_email = models.EmailField()

    class Meta:
        ordering = ["-date"]
