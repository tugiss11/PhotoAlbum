import json
import urllib2

from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from random import randrange

from models import *


def flickr_search(terms):
    url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=24859aa23c48aad43966878ae07f9486&tags="
    for term in terms.split():
        url += term + "+"
    url += "&sort=relevance&media=photos&format=json&nojsoncallback=1"
    result = json.load(urllib2.urlopen(url))
    pagecount = result["photos"]["pages"]
    if pagecount > 1:
        url += "&page=" + str(min(randrange(pagecount), 50))
        result = json.load(urllib2.urlopen(url))
    out = []
    for photo in result["photos"]["photo"]:
        urlbody = "http://farm" + str(photo["farm"]) + ".staticflickr.com/" + str(photo["server"]) + "/" + str(photo["id"]) + "_" + str(photo["secret"])
        thumb_url = urlbody + "_m.jpg" # See sizes in the end of the document
        url = urlbody + ".jpg"

        out.append({"url" : url,
                    "thumb_url": thumb_url,
                    "title": photo["title"],
                    "id": photo["id"]})
    return out

@csrf_protect
def flickr_search_view(request):
    if not request.user.is_authenticated() or request.method == 'GET':
        raise PermissionDenied()

    q = request.POST
    try:
        data = {"image_id": q["image_id"]}
        data["flickr"] = flickr_search(q["terms"])
        image = AlbumImage.objects.get(image_id = q["image_id"])
        data["album_url"] = "/album/" + str(image.page.album.album_id) + "/" + str(image.page.idx)
        return render_to_response('flickr_search.html', data, context_instance=RequestContext(request))

    except Exception as e:
        raise Http404

"""
The letter suffixes are as follows:
s   small square 75x75
q   large square 150x150
t   thumbnail, 100 on longest side
m   small, 240 on longest side
n   small, 320 on longest side
-   medium, 500 on longest side
z   medium 640, 640 on longest side
c   medium 800, 800 on longest side
b   large, 1024 on longest side*
o   original image, either a jpg, gif or png, depending on source format
"""