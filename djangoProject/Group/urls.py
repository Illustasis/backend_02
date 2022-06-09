from django.urls import path
from .views import *

urlpatterns = [
    path('hot', hotgroup),
    path('add', add_kind),
    path('delete', delete_kind),
    path('search', search_kind),
    path('upload', upload_passage),
    path('hotpassage',hotpassage),
    path('hot_article', hot_article),
    path('new_article', new_article),
    path('biggroup', big),
    path('mygroup', myGroup),
    path('detail', detail),
]