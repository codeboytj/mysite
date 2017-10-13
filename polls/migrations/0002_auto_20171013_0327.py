# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='extra',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(related_name='choices', to='polls.Question'),
        ),
    ]
