# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20150402_2012'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='update_defaults',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
