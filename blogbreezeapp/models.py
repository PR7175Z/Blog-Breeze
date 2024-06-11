from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

class Category(models.Model):
  name = models.CharField(max_length=30)
  content = HTMLField(default = '')
  featuredimage = models.ImageField(upload_to='uploads/', default=0) 
  author = models.ForeignKey(User, on_delete=models.CASCADE, default='')

  def __str__(self):
    return f'{self.name}'

class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default="", null=False, blank=True, unique=True)
    publishdate = models.DateTimeField(auto_now_add=True)
    authorid = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    featuredimage = models.ImageField(upload_to='uploads/', default=0) 
    content = HTMLField(default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', default=1)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure the slug is unique
            unique_slug = self.slug
            num = 1
            while Blog.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{self.slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)