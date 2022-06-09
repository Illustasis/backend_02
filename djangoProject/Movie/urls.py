from django.urls import path
from .views import *

urlpatterns = [
    path('detail', detail),
    path('collect',collect),
    path('uncollect',uncollect),
    path('hot', hot),
    path('high', high),
    path('star',star),
    path('collection', collection),
    path('hotpassage', hotcomment),
    path('commentMovie', commentMovie),
    path('article/hot', hot_article),
    path('article/new', new_article),
    path('mypassage', my_article),
]
