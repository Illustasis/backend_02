from django.urls import path
from .views import *

urlpatterns = [
    path('detail', detail),
    path('collect',collect),
    path('uncollect',uncollect),
    path('hot', hot),
    path('high', high),
    path('collection', collection),
    path('star',star),
    path('commentTele', commentTele),
    path('mypassage', my_article),
    path('hot_article', hot_article),
    path('new_article', new_article),
]