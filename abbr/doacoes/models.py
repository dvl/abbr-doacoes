import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models


class Doacao(models.Model):
    CPF = 'cpf'
    CNPJ = 'cnpj'

    TIPO_DOCUMENTO_CHOICES = (
        (CPF, 'CPF'),
        (CNPJ, 'CNPJ'),
    )

    CARTAO_CREDITO = 'cartao'
    BOLETO_BANCARIO = 'boleto'
    PAYPAL = 'paypal'

    TIPO_FORMA_PAGAMENTO = (
        (CARTAO_CREDITO, 'Cartão de Crédito'),
        (BOLETO_BANCARIO, 'Boleto Bancário'),
        (PAYPAL, 'PayPal'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    nome = models.CharField(
        verbose_name='Nome Completo',
        max_length=90,
    )

    email = models.EmailField(
        verbose_name='E-mail',
    )

    tipo_documento = models.CharField(
        verbose_name='Tipo do Documento',
        choices=TIPO_DOCUMENTO_CHOICES,
        max_length=15,
    )

    numero_documento = models.CharField(
        verbose_name='Número do Documento',
        max_length=15,
    )

    valor_doacao = models.DecimalField(
        verbose_name='Valor da Doação (R$)',
        max_digits=6,
        decimal_places=2
    )

    forma_pagamento = models.CharField(
        verbose_name='Forma de Pagamento',
        choices=TIPO_FORMA_PAGAMENTO,
        max_length=6,
    )

    recorrencia = models.BooleanField(
        verbose_name='Doação Mensal',
        default=False,
    )

    resposta_gateway = JSONField(
        verbose_name='Resposta da Mundipagg',
        null=True,
        editable=False,
    )

    criado_em = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True,
    )

    atualizado_em = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'doação'
        verbose_name_plural = 'doações'

        required_db_vendor = 'postgresql'

    def __str__(self):
        return '{}'.format(self.pk)
