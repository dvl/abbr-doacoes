# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-27 01:25
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doacao',
            name='resposta_gateway',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]