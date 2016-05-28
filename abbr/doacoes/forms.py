from django import forms
from django.utils import timezone

from abbr.doacoes.models import Doacao


class DoacaoForm(forms.ModelForm):

    class Meta:
        model = Doacao

        fields = (
            'nome', 'email', 'tipo_documento', 'numero_documento',
            'valor_doacao', 'forma_pagamento', 'recorrencia',
        )

        widgets = {
            'valor_doacao': forms.NumberInput(attrs={'step': '1'}),
            'forma_pagamento': forms.HiddenInput(),
        }


class PagamentoForm(forms.ModelForm):
    VISA = "Visa"
    MASTERCARD = "Mastercard"
    HIPERCARD = "Hipercard"
    AMEX = "Amex"
    DINERS = "Diners"
    ELO = "Elo"
    AURA = "Aura"
    DISCOVER = "Discover"
    CASASHOW = "CasaShow"
    HUGCARD = "HugCard"

    BANDEIRA_CHOICES = (
        (VISA, "Visa"),
        (MASTERCARD, "Mastercard"),
        (HIPERCARD, "Hipercard"),
        (AMEX, "Amex"),
        (DINERS, "Diners"),
        (ELO, "Elo"),
        (AURA, "Aura"),
        (DISCOVER, "Discover"),
        (CASASHOW, "CasaShow"),
        (HUGCARD, "HugCard"),
    )

    nome_titular = forms.CharField(
        label='Nome do titular do cartão de crédito',
    )

    numero_cartao = forms.CharField(
        label='Número do cartão de crédito',
    )

    bandeira = forms.ChoiceField(
        label='Bandeira do cartão de crédito',
        choices=BANDEIRA_CHOICES,
    )

    validade_mes = forms.IntegerField(
        label='Validade (Mês)',
    )

    validade_ano = forms.IntegerField(
        label='Validade (Ano)',
    )

    verificador = forms.IntegerField(
        label='Verificador',
    )

    class Meta:
        model = Doacao
        fields = []  # Nenhum

    def clean_validade_mes(self):
        data = self.cleaned_data['validade_mes']

        if data < 1 or data > 12:
            raise forms.ValidationError('Insira um mês válido.')

        return data

    def clean_validade_ano(self):
        data = self.cleaned_data['validade_ano']

        if data < timezone.now().year or len(str(data)) != 4:
            raise forms.ValidationError('Insira um ano válido.')

        return data

    def clean_verificador(self):
        data = self.cleaned_data['verificador']

        if len(str(data)) not in [3, 4]:
            raise forms.ValidationError('Insira um verificador válido.')

        return data
