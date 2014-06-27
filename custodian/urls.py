from django.conf.urls import patterns, include, url
from django.contrib import admin

from core import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'custodian.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/dashboard/$',  views.dashboard),
    url(r'^admin/', include(admin.site.urls)),
)
