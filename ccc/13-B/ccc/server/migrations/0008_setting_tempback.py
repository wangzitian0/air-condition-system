# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='tempback',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
