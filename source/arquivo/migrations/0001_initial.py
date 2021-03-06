# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 14:45
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('arquivo', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
