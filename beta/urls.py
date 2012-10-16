from django.conf.urls import patterns, include, url
import os.path
static = os.path.join(
    os.path.dirname(__file__),'static'
)
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^beta/', include('beta.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','info.views.home',name='home'),
    url(r'^user/(\w+)/$','info.views.user_page', name='user_page'),
    url(r'^login/$','django.contrib.auth.views.login'),
    url(r'^logout/$','info.views.logout_page'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',
    {'document_root': static}),
    url(r'^register/$', 'info.views.register_page'),
    url(r'^about/$','info.views.about'),
    url(r'^interest/save/$','info.views.interest_save_page'),
    url(r'^interest/delete/$','info.views.delete_interest'),
    url(r'^edit/$','info.views.edit_profile'),
    url(r'^koinbox/$','info.views.koinbox')
)
