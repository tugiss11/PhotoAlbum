from django.shortcuts import render, render_to_response
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

def albumView(request, album_id, page = 0):
    data = {}
    query = Album.objects.filter(album_id = album_id)
    if len(query) == 0:
        raise Http404
    data["album"] = query[0]
    data["page"] = query[0].pages.filter(idx = page)[0]
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
            Album.objects.filter(album_id = q["album_id"]).delete()
            if request.method == "GET":
                return mainView(request)
            elif request.method == "POST":
                return # What to return?

    # elif q.action == "add_page":
    #     if "album_id" in q and ""

    raise Http404