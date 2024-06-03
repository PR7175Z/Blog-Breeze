from django.contrib import admin
from .models import Blog, Category

# admin.site.register(Blog)

# Register your models here.

class blogadmin(admin.ModelAdmin):
  list_display = ("title", "publishdate", "authorid")
  prepopulated_fields = {"slug": ("title",)}
  
admin.site.register(Blog, blogadmin)

class blogcategory(admin.ModelAdmin):
  list_display = ("name", "content")
  
admin.site.register(Category, blogcategory)