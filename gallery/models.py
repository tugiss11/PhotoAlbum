from django.db import models
from layouts.layout_info import PAGE_LAYOUTS, NAME_DB_MAX_LENGTH

import uuid

def createAlbum(title, owner = None):
    album = Album(title = title)
    album.save()
    return album

class Album(models.Model):
    title = models.CharField(max_length = 256)
    #owner = TODO
    unique_url = models.CharField(max_length = 8, unique = True, default=lambda:str(uuid.uuid4()))

    def addPage(self, layout):
        page = AlbumPage(album = self, layout = layout, idx = len(self.pages.all()))
        page.save()
        for i in xrange(10):
            page.addImage()
        page.save()

        return page # Maybe someone is interested in this

class AlbumPage(models.Model):
    idx = models.IntegerField()
    album = models.ForeignKey(Album, related_name = "pages")
    layout = models.CharField(max_length = NAME_DB_MAX_LENGTH, choices = PAGE_LAYOUTS, default = PAGE_LAYOUTS[0])

    def addImage(self):
        image = AlbumImage(page = self, idx = len(self.images.all()))
        image.save()

        return image # Maybe someone is interested in this

class AlbumImage(models.Model):
    idx = models.IntegerField()
    page = models.ForeignKey(AlbumPage, related_name = "images")
    url = models.URLField(default = "")
    caption = models.TextField(default = "")