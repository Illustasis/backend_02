from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.contrib.staticfiles.urls import static
from . import settings
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include(('System.urls', 'System'))),
    path('api/book/', include(('Book.urls', 'Book'))),
    path('api/topic/', include(('Topic.urls', 'Topic'))),
    path('api/group/', include(('Group.urls', 'Group'))),
    path('api/movie/', include(('Movie.urls', 'Movie'))),
    path('api/tele/', include(('Tele.urls', 'Tele'))),
    path('api/passage/', include(('Passage.urls', 'Passage'))),
    path('api/photo/', include(('Photo.urls', 'Photo'))),
    path('api/user/', include(('User.urls', 'User'))),
    path('upload/<path>',serve,{'document_root': settings.UPLOAD_FILE}),
    path('api/search/', include(('Search.urls', 'Search'))),
]
