from django.urls import path
from .views import *

urlpatterns = [
    path('get_code', get_code),
    path('register', register),  # 指定register函数的路由为register
    path('login', login),
    path('uploadbook', savebook),
    path('uploadmovie', savemovie),
    path('uploadtele', savetele),
    path('uploadgroup', savegroup),
    path('uploadtopic', savetopic),
    path('addreport', add_report),
    path('getreport', get_report),
    path('deal_report',deal_report),
]
