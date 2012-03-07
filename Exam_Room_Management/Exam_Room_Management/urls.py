from django.conf.urls.defaults import patterns, include, url
from Exam_Room_Management.App.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^$',main_page),
    (r'^login/$',login_page),
    (r'^login1/$',login1_page),
    (r'^admin/$',admin_page),    
    (r'^student/$',student_page),
    (r'^student/([^/]+)/$',student_info_page),
    (r'^student/addSub/([^/]+)/$',add_exam_subject_page),
    (r'^student/edit/([^/]+)/$',edit_student_info_page),
    (r'^student/deleting/([^/]+)/$',delete_student_info_confirm_page),
    (r'^student/deleted/([^/]+)/$',deleting_student_info_page),
    (r'^subject/$',subject_page),
    (r'^subject/([^/]+)/$',subject_info_page),
    (r'^subject/edit/([^/]+)/$',edit_subject_info_page),
    (r'^subject/deleting/([^/]+)/$',delete_subject_info_confirm_page),
    (r'^subject/deleted/([^/]+)/$',deleting_subject_info_page),
    (r'^room/$',room_page),
    (r'^room/([^/]+)/([^/]+)/([^/]+)/$',room_info_page),
    #(r'^room/seat/([^/]+)/([^/]+)/([^/]+)/$',exam_seat_page),
    (r'^room/edit/([^/]+)/([^/]+)/([^/]+)/$',edit_room_info_page),
    (r'^room/deleting/([^/]+)/([^/]+)/([^/]+)/$',delete_room_info_confirm_page),
    (r'^room/deleted/([^/]+)/([^/]+)/([^/]+)/$',deleting_room_info_page),
    (r'^seat/deleting/([^/]+)/([^/]+)/$',delete_seat_info_confirm_page),
    (r'^seat/deleted/([^/]+)/([^/]+)/$',deleting_seat_info_page),
    # Examples:
    # url(r'^$', 'Exam_Room_Management.views.home', name='home'),
    # url(r'^Exam_Room_Management/', include('Exam_Room_Management.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
