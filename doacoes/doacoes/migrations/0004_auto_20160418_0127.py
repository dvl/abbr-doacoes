# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes', '0003_transacao_cancelado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transacao',
            name='cancelado',
        ),
        migrations.AlterField(
            model_name='transacao',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
