# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cartitem_variations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Cart Item', 'verbose_name_plural': 'Carts Items'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Cart Item', 'verbose_name_plural': 'Carts Items'},
        ),
    ]
