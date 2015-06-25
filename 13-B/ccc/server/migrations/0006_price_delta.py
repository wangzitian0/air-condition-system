# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='delta',
            field=models.FloatField(default=0),
        ),
    ]
