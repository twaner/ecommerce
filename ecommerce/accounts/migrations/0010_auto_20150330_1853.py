# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailconfirmed',
            options={'verbose_name': 'Email Confirmed', 'verbose_name_plural': 'Email Confirmeds'},
        ),
        migrations.AlterModelOptions(
            name='emailmarketingsignup',
            options={'verbose_name': 'Email Marketing Signup', 'verbose_name_plural': 'Email Marketing Signups'},
        ),
        migrations.AlterModelOptions(
            name='useraddress',
            options={'ordering': ['-updated', '-timestamp'], 'verbose_name': 'User Address', 'verbose_name_plural': 'User Addresses'},
        ),
        migrations.AlterModelOptions(
            name='userdefaultaddress',
            options={'verbose_name': 'User Default Address', 'verbose_name_plural': 'User Default Addresses'},
        ),
        migrations.AlterModelOptions(
            name='userstripe',
            options={'verbose_name': 'Stripe User', 'verbose_name_plural': 'Stripe Users'},
        ),
    ]
