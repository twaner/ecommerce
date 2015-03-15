# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_emailconfirmed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailconfirmed',
            old_name='hashkey',
            new_name='activation_key',
        ),
    ]
