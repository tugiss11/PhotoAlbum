from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from models import *

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
    return render_to_response('main.html', data)

def albumView(request, album_id, page = 1):
    data = {}
    album = get_object_or_404(Album, album_id = album_id)
    data["album"] = album
    data["page"] = get_object_or_404(AlbumPage, album = album, idx = page)
    return render_to_response("album_view.html", data)

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
            if request.method == "GET":
                return mainView(request)
            elif request.method == "POST":
                return # What to return?

    elif q["action"] == "remove_album":
        if "album_id" in q:
            get_object_or_404(Album, album_id = q["album_id"]).delete()
            if request.method == "GET":
                return mainView(request)
            elif request.method == "POST":
                return # What to return?

    elif q["action"] == "remove_page":
        if "album_id" in q and "idx" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.pages.filter(idx = q["idx"]).delete()
            album.fixPageNumbers()
            if request.method == "GET":
                return albumView(request, q["album_id"], max(1, int(q["idx"]) - 1))
            elif request.method == "POST":
                return # What to return?

    elif q["action"] == "add_page":
        if "album_id" in q and "layout" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.addPage(q["layout"])
            if request.method == "GET":
                return albumView(request, q["album_id"], len(album.pages.all()))
            elif request.method == "POST":
                return # What to return?

    elif q["action"] == "fix_page_numbers":
        if "album_id" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.fixPageNumbers()
            if request.method == "GET":
                return albumView(request, q["album_id"])
            elif request.method == "POST":
                return # What to return?


    raise Http404