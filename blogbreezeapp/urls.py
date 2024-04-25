from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpageloader, name='members'),
]