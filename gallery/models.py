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
    album_id = models.CharField(max_length = 36, unique = True, default=lambda:str(uuid.uuid4()))

    def addPage(self, layout):
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

class AlbumImage(models.Model):
    idx = models.IntegerField()
    page = models.ForeignKey(AlbumPage, related_name = "images")
    url = models.URLField(default = "")
    caption = models.TextField(default = "")
    image_id = models.CharField(max_length = 36, unique = True, default=lambda:str(uuid.uuid4()))