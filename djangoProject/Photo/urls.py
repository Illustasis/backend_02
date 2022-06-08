from django.urls import path
from .views import *

urlpatterns = [
    path('upload_photo', upload_photo),
    path('get_photo', get_photo),
]