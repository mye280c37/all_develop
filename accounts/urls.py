from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
]