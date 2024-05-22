from django.http import HttpResponse
from django.template import loader
from .models import Blog
from django.shortcuts import render

def indexpageloader(request):
  blogs = Blog.objects.all().order_by('-publishdate').values()
  template = loader.get_template('index.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))

def bloglistingloader(request):
  blogs = Blog.objects.all().order_by('-publishdate').values()
  template = loader.get_template('bloglisting.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  blogsingle = Blog.objects.get(id=id)
  other_blogs = Blog.objects.exclude(id=id).order_by('?')[:3]
  template = loader.get_template('blogsingle.html')
  context = {
    'blogsingle': blogsingle,
    'otherblog':other_blogs,
  }
  return HttpResponse(template.render(context, request))

def contactpageloader(request):
  template = loader.get_template('contact.html')
  return HttpResponse(template.render())