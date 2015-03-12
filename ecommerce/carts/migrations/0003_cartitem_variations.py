# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_variation_category'),
        ('carts', '0002_cartitem_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(to='products.Variation', null=True, blank=True),
            preserve_default=True,
        ),
    ]
