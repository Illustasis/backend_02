from django.urls import path
from .views import *

urlpatterns = [
    path('detail', detail),
    path('isadmin',isadmin)
]