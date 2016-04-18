from django.contrib.postgres.fields import JSONField
from django.db import models


class Transacao(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)

    data = JSONField()

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = [
            '-criado_em',
        ]

    def __str__(self):
        return str(self.id)

    def order_key(self):
        return self.data['OrderResult'].get('OrderKey')

    def create_date(self):
        return self.data['OrderResult'].get('CreateDate')

    def order_reference(self):
        return self.data['OrderResult'].get('OrderReference')

    def buyer_key(self):
        return self.data['BuyerKey']

    def request_key(self):
        return self.data['RequestKey']

    def success(self):
        return self.data.get('ErrorReport') is None
    success.boolean = True

    def boleto_url(self):
        try:
            return self.data['BoletoTransactionResultCollection'][0]['BoletoUrl']
        except (KeyError, IndexError, TypeError):
            return None
