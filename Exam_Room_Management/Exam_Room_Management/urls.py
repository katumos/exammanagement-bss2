from django.conf.urls.defaults import patterns, include, url
from Exam_Room_Management.App.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',main_page),
    (r'^admin/$',admin_page),
    (r'^student/$',student_page),
    (r'^student/([^/]+)/$',student_info_page),
    (r'^student/edit/([^/]+)/$',edit_student_info_page),
    (r'^student/delete/([^/]+)/$',delete_student_info_page),
    (r'^subject/$',subject_page),
    (r'^subject/([^/]+)/$',subject_info_page),
    (r'^subject/edit/([^/]+)/$',edit_subject_info_page),
    (r'^subject/delete/([^/]+)/$',delete_subject_info_page),
    (r'^room/$',room_page),
    (r'^room/([^/]+)/$',room_info_page),
    (r'^room/edit/([^/]+)/$',edit_room_info_page),
    (r'^room/delete/([^/]+)/$',delete_room_info_page),
    # Examples:
    # url(r'^$', 'Exam_Room_Management.views.home', name='home'),
    # url(r'^Exam_Room_Management/', include('Exam_Room_Management.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
