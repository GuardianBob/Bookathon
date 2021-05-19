from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('register', views.register),
    path('user_register', views.new_registration, name='user_register'),
    path('add_user', views.add_new_user, name='add_user'),
    path('user_validate', views.validate_login),
    path('logout', views.logout_view, name='logout'),
    ]