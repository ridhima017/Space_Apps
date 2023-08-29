from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('monitor_map/', views.monitor_map, name='monitor_map'),
]