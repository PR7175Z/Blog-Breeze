# Generated by Django 5.0.4 on 2024-05-17 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogbreezeapp', '0002_blog_authorid'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='featuredimage',
            field=models.ImageField(default=0, upload_to='uploads/'),
        ),
    ]
