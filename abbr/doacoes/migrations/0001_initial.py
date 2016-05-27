# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-27 01:24
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doacao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=90, verbose_name='Nome Completo')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('tipo_documento', models.CharField(choices=[('cpf', 'CPF'), ('cnpj', 'CNPJ')], max_length=15, verbose_name='Tipo do Documento')),
                ('numero_documento', models.CharField(max_length=15, verbose_name='Número do Documento')),
                ('valor_doacao', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor da Doação (R$)')),
                ('forma_pagamento', models.CharField(choices=[('cartao', 'Cartão de Crédito'), ('boleto', 'Boleto Bancário'), ('paypal', 'PayPal')], max_length=6, verbose_name='Forma de Pagamento')),
                ('recorrencia', models.BooleanField(default=False, verbose_name='Doação Mensal')),
                ('resposta_gateway', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
