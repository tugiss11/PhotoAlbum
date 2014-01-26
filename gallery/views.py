from django.shortcuts import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.forms.models import modelform_factory
from django.contrib import auth
from django.core.context_processors import csrf
from models import *
from forms import *
import payments

def indexView(request): #add by liang
    return render_to_response('index.html',context_instance=RequestContext(request))

def mainView(request):
    data = {}
    albums = []
    user = auth.get_user(request)
    queried_albums = None
    if not request.user.is_authenticated():
        queried_albums = Album.objects.all()
    else:
        queried_albums = user.Albums.all()
    for album in queried_albums:
        a = {}
        a["title"] = album.title
        a["page_count"] = len(album.pages.all())
        a["album_id"] = album.album_id
        albums.append(a)

    data["albums"] = albums
    data["page_count"] = len(AlbumPage.objects.all())
    data["image_count"] = len(AlbumImage.objects.all())
    data["album_count"] = len(Album.objects.all())

    data["new_album_form"] = modelform_factory(Album,
                                               fields=["title"])
    return render_to_response('main.html', data, context_instance=RequestContext(request))

def albumView(request, album_id, page = 1):
    data = {}

    data["image_url_form"] = modelform_factory(AlbumImage,
                                               fields=["url"])
    data["add_page_form"] = modelform_factory(AlbumPage,
                                              fields=["layout"])
    data["delete_page_form"] = modelform_factory(AlbumPage, fields=[])

    album = get_object_or_404(Album, album_id = album_id)
    data["album"] = album
    try:
        data["page"] = AlbumPage.objects.get(album = album, idx = page)
    except:
        pass
    return render_to_response("album_view.html", data, context_instance=RequestContext(request))

def modify(request):
    # TODO: Check login
    q = None
    if request.method == 'GET':
        q = request.GET
    elif request.method == 'POST':
        q = request.POST

    if q["action"] == "create_album":
        if "title" in q:
            createAlbum(q["title"], request.user)
            return redirect("gallery.views.mainView")

    elif q["action"] == "remove_album":
        if "album_id" in q:
            get_object_or_404(Album, album_id = q["album_id"]).delete()
            return redirect("gallery.views.mainView")

    elif q["action"] == "remove_page":
        if "album_id" in q and "idx" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.pages.filter(idx = q["idx"]).delete()
            album.fixPageNumbers()
            return redirect("gallery.views.albumView", q["album_id"], max(1, int(q["idx"]) - 1))

    elif q["action"] == "add_page":
        if "album_id" in q and "layout" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.addPage(q["layout"])
            return redirect("gallery.views.albumView", q["album_id"], len(album.pages.all()))

    elif q["action"] == "fix_page_numbers":
        if "album_id" in q:
            album = get_object_or_404(Album, album_id = q["album_id"])
            album.fixPageNumbers()
            return redirect("gallery.views.albumView", q["album_id"])

    elif q["action"] == "modify_image_url":
        if "image_id" in q and "url" in q:
            image = get_object_or_404(AlbumImage, image_id = q["image_id"])
            image.url = q["url"]
            image.save()
            print "redirecting"
            return redirect("gallery.views.albumView", image.page.album.album_id, image.page.idx)

    elif q["action"] == "remove_order":
        if "order_id" in q:
            try:
                AlbumOrder.objects.get(order_id = q["order_id"]).delete()
            except:
                pass
        return redirect("/my_orders")

    raise Http404


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def register(request):
    return render_to_response('register.html')

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/main') # The page should redirct to MAIN page. so the following tag full_name should bu changed.
    else:
        return HttpResponseRedirect('/invalid')

def loggedin(request):
    return render_to_response('loggedin.html', {'full_name': request.user.username})

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def invalid_login(request):
    return render_to_response('invalid.html')

def orderAlbumView(request, album_id):
    if not request.user.is_authenticated():
        print("not autheticated")
        raise Http404

    album = get_object_or_404(Album, album_id = album_id)
    user = auth.get_user(request)

    if request.method == "POST":
        # Validating form
        order_form = AlbumOrderForm(request.POST)
        if order_form.is_valid():
            q = request.POST
            order_entry = AlbumOrder(price = len(album.pages.all()) * 2.1, 
                                     owner = user, 
                                     album = album,
                                     client_name = q["client_name"],
                                     client_address = q["client_address"],
                                     client_email = q["client_email"])
            order_entry.save()
            return redirect("/order_check/" + order_entry.order_id)

    else:
        order_form = AlbumOrderForm()
    data = {}

    data["form"] = order_form
    data["album"] = album
    data["price"] = len(album.pages.all()) * 2.1
    return render_to_response('order_album.html', data, context_instance=RequestContext(request))

def orderAlbumCheckView(request, order_id):
    if not request.user.is_authenticated():
        raise Http404

    q = request.GET
    user = auth.get_user(request)
    order_entry = get_object_or_404(AlbumOrder, owner = user, order_id = order_id)
    album = order_entry.album
    data = {}

    data["album"] = album
    data["order"] = order_entry
    data["seller_id"] = payments.SELLER_ID
    data["checksum"] = payments.generate_payment_checksum(order_entry.order_id, order_entry.price)

    return render_to_response("order_album_check.html", data, context_instance=RequestContext(request))

def orderAlbumSuccessView(request):
    # TODO: Only allow POST
    q = request.GET
    checksum = payments.generate_payment_succesfull_checksum(q["pid"], q["ref"])
    if checksum != q["checksum"]:
        raise Http404

    order_entry = get_object_or_404(AlbumOrder, order_id = q["pid"])
    order_entry.payment_reference_number = q["ref"]
    order_entry.payment_succesful = True
    order_entry.save()

    return redirect("/my_orders", "success")

def orderAlbumFailView(request):
    return redirect("/my_orders", "failed")

def myOrdersView(request, payment_state = ""):
    print("payment state: " + payment_state)
    if not request.user.is_authenticated():
        raise Http404

    user = auth.get_user(request)
    data = {}
    orders = AlbumOrder.objects.filter(owner = user)

    data["orders"] = orders
    data["pament_state"] = payment_state

    return render_to_response("my_orders.html", data, context_instance=RequestContext(request))