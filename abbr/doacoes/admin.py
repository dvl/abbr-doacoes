from django.contrib import admin

from abbr.doacoes.models import Doacao


@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'email',
        'tipo_documento',
        'numero_documento',
        'valor_doacao',
        'forma_pagamento',
        'enviado_gateway',
        'status_pagamento',
        'recorrencia',
        'criado_em',
        'atualizado_em',
    )

    search_fields = (
        'nome',
        'email',
        'tipo_documento',
        'numero_documento',
        'valor_doacao',
        'forma_pagamento',
        'recorrencia',
        'criado_em',
        'atualizado_em',
    )

    list_filter = (
        'tipo_documento',
        'forma_pagamento',
        'recorrencia',
    )

    fieldsets = (
        (None, {
            'fields': (
                'id',
                'criado_em',
                'atualizado_em',
            )
        }),
        ('Dados do Doador', {
            'fields': (
                'nome',
                'email',
                'tipo_documento',
                'numero_documento',
            )
        }),
        ('Dados da Doação', {
            'fields': (
                'valor_doacao',
                'forma_pagamento',
                'recorrencia',
            )
        }),
        ('Informação do gateway de pagamento', {
            'fields': (
                'resposta_gateway',
                'notificacao_gateway',
            ),
            'classes': (
                'collapse',
            ),
        }),
    )

    class Media:
        css = {
            'all': (
                '//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/styles/default.min.css',
            )
        }

        js = (
            '//cdnjs.cloudflare.com/ajax/libs/highlight.js/9.4.0/highlight.min.js',
            'js/admin.js',
        )

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
