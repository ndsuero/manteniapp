# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',       views.register,      name='register'),
    path('profile/',        views.profile_view,  name='profile'),
    path('profile/edit/',   views.profile_edit,  name='profile_edit'),
    path('users/',          views.user_list,      name='user_list'),
    path('users/<int:user_id>/promote/', 
         views.promote_user, name='promote_user'),
]