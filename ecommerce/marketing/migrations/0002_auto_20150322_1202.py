# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import marketing.models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('image', models.ImageField(upload_to=marketing.models.slider_upload)),
                ('header_text', models.CharField(max_length=120, null=True, blank=True)),
                ('text', models.CharField(max_length=120, null=True, blank=True)),
            ],
            options={
                'ordering': ['-start_date', '-end_date'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='marketingmessage',
            options={'ordering': ['-start_date', '-end_date']},
        ),
    ]
