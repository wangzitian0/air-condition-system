# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20150614_0257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('speed', models.CharField(default=b'0', max_length=1, choices=[(b'0', b'UNSET'), (b'1', b'LOW'), (b'2', b'MIDDLE'), (b'3', b'HIGH')])),
                ('mode', models.CharField(default=b'U', max_length=1, choices=[(b'U', b'UNSET'), (b'C', b'COLD'), (b'H', b'HOT')])),
                ('price', models.FloatField()),
            ],
        ),
    ]
