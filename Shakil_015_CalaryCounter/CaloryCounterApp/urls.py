from django.urls import path
from .views import *

urlpatterns = [
    path('register/',register_view, name='register_view'),
    path('',login_view, name='login_view'),
    path('dashboard/',dashboard, name='dashboard'),
    
    path('profile_view/',profile_view, name='profile_view'),
    path('profile_update/',profile_update, name='profile_update'),
    
    path('add_calorie/',add_calorie, name='add_calorie'),
    path('update_calorie/<str:pk>/',update_calorie, name='update_calorie'),
    path('delete_calorie/<str:pk>/',delete_calorie, name='delete_calorie'),
    
    path('logout_view/',logout_view, name='logout_view'),
]