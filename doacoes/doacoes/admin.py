from django.contrib import admin

from . import models


@admin.register(models.Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'criado_em',
        'success',
    ]

    readonly_fields = [
        'atualizado_em',
        'boleto_url',
        'buyer_key',
        'create_date',
        'criado_em',
        'data',
        'order_key',
        'order_reference',
        'request_key',
        'success',
    ]

    fieldsets = (
        ('Dados da Transação', {
            'fields': (
                'success',
                'order_key',
                'buyer_key',
                'order_reference',
                'create_date',
                'request_key',
                'boleto_url',
            ),
        }),
        ('Metadados', {
            'fields': (
                'data',
                'criado_em',
                'atualizado_em',
            ),
        }),
    )
