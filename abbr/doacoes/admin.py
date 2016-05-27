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

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
