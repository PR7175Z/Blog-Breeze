from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpageloader, name='indexpage'),
    path('bloglisting', views.bloglistingloader, name='bloglisting'),
]