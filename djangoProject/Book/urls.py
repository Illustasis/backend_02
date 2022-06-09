from django.urls import path
from .views import *

urlpatterns = [
    path('detail', detail),
    path('collect',collect),
    path('uncollect',uncollect),
    path('article/hot', hot_article),
    path('article/new', new_article),
    path('hot', hotbook),
    path('high', highbook),
    path('collection', book_collection),
    path('star', star),
    path('passage', commentBook),
    path('hotpassage',hotcomment),
    path('mypassage',my_article),
    path('recommend',recommend),
]
