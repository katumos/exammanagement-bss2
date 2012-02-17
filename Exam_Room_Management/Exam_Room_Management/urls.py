from django.conf.urls.defaults import patterns, include, url
from Exam_Room_Management.App.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',main_page),
    (r'^admin/$',admin_page),
    (r'^student/$',student_page),
    (r'test/$',my_view),
    (r'test2/$',my_view2),
    # Examples:
    # url(r'^$', 'Exam_Room_Management.views.home', name='home'),
    # url(r'^Exam_Room_Management/', include('Exam_Room_Management.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
