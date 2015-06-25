# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20150610_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='connected',
            field=models.CharField(default=b'F', max_length=1, choices=[(b'U', b'UNSET'), (b'C', b'COLD'), (b'H', b'HOT')]),
        ),
        migrations.AlterField(
            model_name='client',
            name='sleep',
            field=models.CharField(default=b'F', max_length=1, choices=[(b'U', b'UNSET'), (b'C', b'COLD'), (b'H', b'HOT')]),
        ),
    ]
