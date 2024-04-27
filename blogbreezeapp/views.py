from django.http import HttpResponse
from django.template import loader
from .models import Blog

def indexpageloader(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def bloglistingloader(request):
  blogs = Blog.objects.all().values()
  template = loader.get_template('index.html')
  context = {
    'blogs': blogs,
  }
  return HttpResponse(template.render(context, request))