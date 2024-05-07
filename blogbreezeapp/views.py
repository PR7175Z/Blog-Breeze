from django.http import HttpResponse
from django.template import loader
from .models import Blog
from django.shortcuts import render

def indexpageloader(request):
  blogs = Blog.objects.all().values()
  template = loader.get_template('index.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))

def bloglistingloader(request):
  blogs = Blog.objects.all().values()
  template = loader.get_template('bloglisting.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))

def contactpageloader(request):
  template = loader.get_template('contact.html')
  return HttpResponse(template.render())