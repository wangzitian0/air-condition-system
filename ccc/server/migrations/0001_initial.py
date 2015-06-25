# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_num', models.IntegerField(unique=True)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('temp_now', models.FloatField()),
                ('temp_set', models.FloatField()),
                ('speed', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'LOW'), (b'2', b'MIDDLE'), (b'3', b'HIGH')])),
                ('mode', models.CharField(default=b'U', max_length=1, choices=[(b'U', b'UNSET'), (b'C', b'COLD'), (b'H', b'HOT')])),
                ('connected', models.BooleanField()),
                ('sleep', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('room_num', models.IntegerField()),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('speed', models.CharField(default=b'1', max_length=1, choices=[(b'1', b'LOW'), (b'2', b'MIDDLE'), (b'3', b'HIGH')])),
                ('mode', models.CharField(default=b'U', max_length=1, choices=[(b'U', b'UNSET'), (b'C', b'COLD'), (b'H', b'HOT')])),
            ],
        ),
    ]
