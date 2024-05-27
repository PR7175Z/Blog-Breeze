from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User

class Category(models.Model):
  name = models.CharField(max_length=30)
  content = HTMLField(default = '')

  def __str__(self):
    return f'{self.name}'

class Blog(models.Model):
  title = models.CharField(max_length=255)
  slug = models.SlugField(default="", null=False)
  publishdate = models.DateTimeField(auto_now_add=True)
  authorid = models.IntegerField(default=0)
  featuredimage = models.ImageField(upload_to ='uploads/', default=0) 
  content = HTMLField(default='')
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', default=1)

  def __str__(self):
    return f'{self.title}'
  
class User(models.Model):
  username = models.CharField(max_length=50, default='')
  first_name = models.CharField(max_length=50, default='')
  last_name = models.CharField(max_length=50, default='')
  password = models.CharField(max_length=50, default='')
  profilepic = models.ImageField(upload_to ='uploads/', default=0) 

  def __str__(self):
    return f'{self.username}'