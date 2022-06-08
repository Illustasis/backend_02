import os,sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
sys.path.append('/var/www/html/safe')
application = get_wsgi_application()
