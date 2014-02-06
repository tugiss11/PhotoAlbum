from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import gallery.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'group7.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'gallery.views.indexView'),#change by liang
    url(r'^register/$', 'gallery.views.register'),#add register url
    url(r'^newuser/$', 'gallery.views.newuser'),
    url(r'^main$', 'gallery.views.mainView'),
    url(r'^album/([-\w]+)/$', 'gallery.views.albumView'),
    url(r'^album/([-\w]+)/(\d+)$', 'gallery.views.albumView'),
    url(r'^modify', 'gallery.views.modify'),
    url(r'^query', 'gallery.views.query_view'),
    url(r'^login/$', 'gallery.views.login'),
    url(r'logout/$', 'gallery.views.logout'),
    url(r'auth/$', 'gallery.views.auth_view'),
    url(r'loggedin/$', 'gallery.views.loggedin'),
    url(r'invalid/$', 'gallery.views.invalid_login'),
    url(r'^order_album/([-\w]+)/$', 'gallery.views.orderAlbumView'),
    url(r'^order_check/([-\w]+)/$', 'gallery.views.orderAlbumCheckView'),
    url(r'^my_orders/$', 'gallery.views.myOrdersView'),
    url(r'^order_succesfull', 'gallery.views.orderAlbumSuccessView'),
    url(r'^order_failed', 'gallery.views.orderAlbumFailView'),
    url(r'^search_flickr$', 'gallery.flickrsupport.flickr_search_view'),

)


