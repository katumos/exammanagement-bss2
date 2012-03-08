import os
import django.core.handlers.wsgi

init django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'pasteurl.settings'
define wsgi app
application = django.core.handlers.wsgi.WSGIHandler()
mount this application at the webroot
applications = { '/': 'application' }



#เป็น fild เรียกใช้ app Djanjo บน dotcloud
