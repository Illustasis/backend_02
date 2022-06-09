from django.urls import path
from .views import *

urlpatterns = [
    path('bookcomment', bookcomment),
    path('moviecomment', moviecomment),
    path('telecomment', telecomment),
    path('dt',dt),
    path('delete',delete),
    path('like',like),
    path('unlike',unlike),
    path('iflike',iflike),
    path('reply', reply),
    path('get_reply', get_reply),
    path('get_message', get_message),
]
