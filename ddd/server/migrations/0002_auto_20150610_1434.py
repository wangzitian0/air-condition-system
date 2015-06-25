# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='speed',
            field=models.CharField(default=b'0', max_length=1, choices=[(b'0', b'UNSET'), (b'1', b'LOW'), (b'2', b'MIDDLE'), (b'3', b'HIGH')]),
        ),
        migrations.AlterField(
            model_name='cost',
            name='speed',
            field=models.CharField(default=b'0', max_length=1, choices=[(b'0', b'UNSET'), (b'1', b'LOW'), (b'2', b'MIDDLE'), (b'3', b'HIGH')]),
        ),
    ]
