from django.urls import path
from .views import *
from system import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration/', views.CustomerCreateView.as_view(), name='registration'),
]
