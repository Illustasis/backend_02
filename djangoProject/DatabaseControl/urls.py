from django.urls import path
from .views import *

urlpatterns = [
    path('delete', delete),
    path('delete_all', delete_all)
]