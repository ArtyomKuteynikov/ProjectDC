from django.urls import path
from .views import *

urlpatterns = [
    path('customer/', customer_info, name='customer_info'),
    path('education/', education_info, name='education_info'),
    path('experience/', experience_info, name='experience_info'),
    path('cv/', cv_info, name='cv_info'),
    path('education/list/', education_list_info, name='education_list_info'),
    path('experience/list/', experience_list_info, name='experience_list_info'),
    path('cv/list/', cv_list_info, name='cv_list_info'),
    path('education/add/', add_education, name='add_education'),
    path('experience/add/', add_experience, name='add_experience'),
    path('cv/create/', create_cv, name='create_cv'),
    path('customer/update/', customer_update, name='customer_update'),
    path('education/update/', education_update, name='education_update'),
    path('experience/update/', experience_update, name='experience_update'),
    path('cv/update/', cv_update, name='cv_update'),
    path('customer/delete/', customer_delete, name='customer_delete'),
    path('education/delete/', education_delete, name='education_delete'),
    path('experience/delete/', experience_delete, name='experience_delete'),
    path('cv/delete/', cv_delete, name='cv_delete'),
    path('cv/detail/', cv_detail, name='cv_detail'),
    path('cv/all/', cv_list, name='cv_list'),
]
