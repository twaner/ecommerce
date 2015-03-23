# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0003_auto_20150322_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='url_link',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
