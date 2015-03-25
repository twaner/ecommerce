# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0006_remove_emailmarketingsignup_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=120)),
                ('address2', models.CharField(max_length=120, null=True, blank=True)),
                ('city', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=120, null=True, blank=True)),
                ('country', models.CharField(max_length=120)),
                ('zipcode', models.CharField(max_length=25)),
                ('phone', models.CharField(max_length=120, null=True, blank=True)),
                ('shipping', models.BooleanField(default=True)),
                ('billing', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserAddress',
                'verbose_name_plural': 'UserAddresss',
            },
            bases=(models.Model,),
        ),
    ]
