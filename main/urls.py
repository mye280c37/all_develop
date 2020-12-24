from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plan/', views.plan, name='plan'),
    path('schedule_inquiry/', views.schedule_inquiry, name='schedule_inquiry'),
    path('input/', views.input, name='input'),
    path('save_input/<int:pk>/', views.save_input, name='save_input'),
    path('look_up/', views.look_up, name='look_up'),
    path('look_up/super/', views.look_up_super, name='look_up_super'),
    path('look_up/super/<username>/', views.look_up_super_detail, name='look_up_detail'),
    path('save_plan/', views.save_plan, name='save_plan'),
    path('input/edit/', views.input_edit, name='input_edit'),
]