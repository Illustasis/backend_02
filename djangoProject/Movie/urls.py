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
    path('commentMovie', commentMovie),
    path('hot_article', hot_article),
    path('new_article', new_article),
    path('mypassage', my_article),
]
