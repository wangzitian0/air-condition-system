# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0008_setting_tempback'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='temp_refresh',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='setting',
            name='tempsleep',
            field=models.FloatField(default=1.5),
        ),
        migrations.AlterField(
            model_name='setting',
            name='maxlinking',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='setting',
            name='normal',
            field=models.FloatField(default=18),
        ),
        migrations.AlterField(
            model_name='setting',
            name='refresh',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='setting',
            name='tempback',
            field=models.FloatField(default=0.2),
        ),
    ]
