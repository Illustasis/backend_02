from django.urls import path
from .views import *

urlpatterns = [
    path('bookcomment', bookcomment),
    path('moviecomment', moviecomment),
    path('telecomment', telecomment),
    path('dt',dt)
]
