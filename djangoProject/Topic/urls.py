from django.urls import path
from .views import *

urlpatterns = [
    path('hot', hot),
    path('random', random),
    path('detail', detail),
    path('collect', collect),
    path('uncollect', uncollect),
    path('collection', collection),
    path('passage', dt),
    path('mypassage',my_article),
    path('hot_article', hot_article),
    path('new_article', new_article),
]