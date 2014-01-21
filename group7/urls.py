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
    url(r'^main$', 'gallery.views.mainView'),
    url(r'^album/([-\w]+)/$', 'gallery.views.albumView'),
    url(r'^album/([-\w]+)/(\d+)$', 'gallery.views.albumView'),
    url(r'^modify', 'gallery.views.modify'),
	url(r'^login/$', 'gallery.views.login'),
    url(r'logout/$', 'gallery.views.logout'),
    url(r'auth/$', 'gallery.views.auth_view'),
    url(r'loggedin/$', 'gallery.views.loggedin'),
    url(r'invalid/$', 'gallery.views.invalid_login'),
)


