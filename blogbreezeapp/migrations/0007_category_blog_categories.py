# Generated by Django 5.0.4 on 2024-05-21 04:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogbreezeapp', '0006_alter_blog_publishdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Descripcion')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='blogbreezeapp.category')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='item', to='blogbreezeapp.category'),
        ),
    ]
