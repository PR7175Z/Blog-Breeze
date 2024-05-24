from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpageloader, name='home'),
    path('blog', views.bloglistingloader, name='blog'),
    path('contact', views.contactpageloader, name='contact'),
    path('blog/<int:id>', views.blogsingle, name='blogsingle'),
]