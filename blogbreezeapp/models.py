from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Blog(models.Model):
  title = models.CharField(max_length=255)
  publishdate = models.DateTimeField()
  authorid = models.IntegerField(default=0)
  featuredimage = models.ImageField(upload_to ='uploads/', default=0) 
  content = HTMLField(default='')

  def __str__(self):
    return f'{self.title}'