# Generated by Django 5.0.4 on 2024-05-24 16:57

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogbreezeapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='content',
            field=tinymce.models.HTMLField(default=''),
        ),
    ]
