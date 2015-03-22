# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_auto_20150322_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slider',
            options={'ordering': ['order', '-start_date', '-end_date']},
        ),
        migrations.AddField(
            model_name='slider',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
