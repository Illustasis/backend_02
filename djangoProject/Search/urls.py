from django.urls import path
from .views import *

urlpatterns = [
    path('book_search', book_search),
    path('movie_search', movie_search),
    path('tele_search', tele_search),
    path('topic_search', topic_search),
    path('group_search', group_search),
    path('article_search', article_search),
]