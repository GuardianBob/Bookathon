from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.auth import views as auth
from django.conf.urls.static import static

# Original urlpatterns:
# urlpatterns = [
#     path('', views.login),
#     path('register', views.register),
#     path('user_register', views.new_registration, name='user_register'),
#     path('add_user', views.add_new_user, name='add_user'),
#     path('user_validate', views.validate_login),
#     path('logout', views.logout_view, name='logout'),
#     ]

urlpatterns = [
    path('', views.index, name ='index'),
    path('login/', views.login, name ='login'),
    path('accounts/login/', views.login),
    path('logout/', views.logout_view, name ='logout'),
    path('register/', views.register, name ='register'),
    path('user_validate', views.validate_login, name='validate_login'),
    path('validate_register/', views.validate_register, name ='validate_register'),
]