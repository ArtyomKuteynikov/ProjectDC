from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('registration/', register, name='registration'),
    path('login/', login, name='login'),
    path('restore_password/', restore_password, name='restore_password'),
    path('check_code/', enter_code, name='check_code'),
    path('reset_password/', change_password, name='reset_password'),
]
