from django.contrib import admin
from .models import Blog

# admin.site.register(Blog)

# Register your models here.

class blogadmin(admin.ModelAdmin):
  list_display = ("title", "publishdate", "authorid")
  
admin.site.register(Blog, blogadmin)