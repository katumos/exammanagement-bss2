from django.conf.urls.defaults import patterns, include, url
from Data.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^$',main),
    ('^Kmutnb/$', form),
    (r'^FormExam/$', out),
    (r'^admin/', include(admin.site.urls)),
)
