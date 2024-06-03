from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
  name = models.CharField(max_length=30)
  content = HTMLField(default = '')
  author = models.ForeignKey(User, on_delete=models.CASCADE, default='')

  def __str__(self):
    return f'{self.name}'

class Blog(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(default="", null=False)
  publishdate = models.DateTimeField(auto_now_add=True)
  authorid = models.ForeignKey(User, on_delete=models.CASCADE, default='')
  featuredimage = models.ImageField(upload_to ='uploads/', default=0) 
  content = HTMLField(default='')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', default=1)

  def __str__(self):
    return f'{self.title}'