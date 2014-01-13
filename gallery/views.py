from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from models import *
from forms import *

def mainView(request):
    data = {}
    albums = []
    for album in Album.objects.all(): # TODO: Only owned!
        a = {}
        a["title"] = album.title
        a["page_count"] = len(album.pages.all())
        a["album_id"] = album.album_id
        albums.append(a)

    data["albums"] = albums
    data["page_count"] = len(AlbumPage.objects.all())
    data["image_count"] = len(AlbumImage.objects.all())
    data["album_count"] = len(Album.objects.all())
    return render_to_response('main.html', data, context_instance=RequestContext(request))

def albumView(request, album_id, page = 1):
    data = {}
    data["image_url_form"] = ImageURLForm()
    album = get_object_or_404(Album, album_id = album_id)
    data["album"] = album
    data["page"] = get_object_or_404(AlbumPage, album = album, idx = page)
    return render_to_response("album_view.html", data, context_instance=RequestContext(request))

def modify(request):
    # TODO: Check login
    q = None
    if request.method == 'GET':
        q = request.GET # This should be removed in future
    elif request.method == 'POST':
        q = request.POST 

    if q["action"] == "create_album":
        if "title" in q:
            createAlbum(q["title"])
            return mainView(request)

    elif q["action"] == "remove_album":
        if "album_id" in q:
            get_object_or_404(Album, album_id = q["album_id"]).delete()
            return mainView(request)

    elif q["action"] == "remove_page":
        if "album_id" in q and "idx" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.pages.filter(idx = q["idx"]).delete()
            album.fixPageNumbers()
            return albumView(request, q["album_id"], max(1, int(q["idx"]) - 1))

    elif q["action"] == "add_page":
        if "album_id" in q and "layout" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.addPage(q["layout"])
            return albumView(request, q["album_id"], len(album.pages.all()))

    elif q["action"] == "fix_page_numbers":
        if "album_id" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.fixPageNumbers()
            return albumView(request, q["album_id"])

    elif q["action"] == "modify_image_url":
        if "image_id" in q and "url" in q:
            image = get_object_or_404(AlbumImage, image_id = q["image_id"])
            image.url = q["url"]
            image.save()
            return albumView(request, image.page.album.album_id, image.page.idx)

    raise Http404