# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20150614_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='connected',
            field=models.CharField(default=b'F', max_length=1, choices=[(b'T', b'True'), (b'F', b'False')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='sleep',
            field=models.CharField(default=b'F', max_length=1, choices=[(b'T', b'True'), (b'F', b'False')]),
        ),
    ]
