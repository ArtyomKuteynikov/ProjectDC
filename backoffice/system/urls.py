from django.urls import path
from .views import *
from system import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration/', views.register, name='registration'),
    path('login/', views.login, name='login'),
    path('restore_password/', views.restore_password, name='restore_password'),
]
