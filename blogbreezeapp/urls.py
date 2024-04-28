from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpageloader, name='home'),
    path('bloglisting', views.bloglistingloader, name='blog'),
]