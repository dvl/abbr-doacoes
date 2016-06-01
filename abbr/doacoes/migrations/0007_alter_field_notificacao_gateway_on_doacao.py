# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 20:19
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doacoes', '0006_add_field_notificacao_gateway_to_doacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doacao',
            name='notificacao_gateway',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list, editable=False, verbose_name='Notificação da Mundipagg'),
        ),
    ]