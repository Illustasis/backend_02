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
]
