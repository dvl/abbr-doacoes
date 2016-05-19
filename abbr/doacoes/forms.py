import re
import uuid

from django.conf import settings
from django import forms
from django.utils import timezone, crypto

from mundipagg_one.data_contracts import (
    boleto_transaction,
    boleto_transaction_options,
    buyer,
    creditcard,
    create_sale_request,
    creditcard_transaction,
    creditcard_transaction_options,
    order,
    recurrency,
)
from mundipagg_one.enum_types import HttpContentType
from mundipagg_one.gateway_service_client import GatewayServiceClient

from . import models


class PagamentoFormBase(forms.ModelForm):
    CPF = 'cpf'
    CNPJ = 'cnpj'

    TIPO_DOCUMENTO_CHOICES = (
        (CPF, 'CPF'),
        (CNPJ, 'CNPJ'),
    )

    PERSON_TYPE = {
        CPF: 'Person',
        CNPJ: 'Company',
    }

    nome = forms.CharField()
    email = forms.EmailField()

    tipo_documento = forms.ChoiceField(TIPO_DOCUMENTO_CHOICES)
    numero_documento = forms.CharField()

    valor = forms.IntegerField()

    class Meta:
        model = models.Transacao
        fields = []

    def clean_numero_documento(self):
        data = self.cleaned_data['numero_documento']
        data = re.sub(r'\W+', '', data)

        return data

    def get_transaction_collection(self):
        raise NotImplemented

    def clean(self):
        cleaned_data = super().clean()

        buyer_data = buyer(
            name=cleaned_data['nome'],
            email=cleaned_data['email'],
            document_type=cleaned_data['tipo_documento'],
            document_number=cleaned_data['numero_documento'],
            person_type=self.PERSON_TYPE[cleaned_data['tipo_documento']],
        )

        options_request = order(order_reference=self.instance.data)

        field, transaction_collection = self.get_transaction_collection(cleaned_data)

        request = create_sale_request(**{
            field: transaction_collection,
            'order': options_request,
            'buyer': buyer_data,
        })

        merchant_key = settings.MUNDIPAGG_API_KEY
        end_point = settings.MUNDIPAGG_API_ENDPOINT

        service_client = GatewayServiceClient(
            merchant_key,
            settings.MUNDIPAGG_API_ENVIRONMENT,
            HttpContentType.json,
            end_point,
        )

        http_response = service_client.sale.create_with_request(
            create_sale_request=request
        )

        json_response = http_response.json()

        errors = json_response.get('ErrorReport')

        if errors:
            raise forms.ValidationError([e['Description'] for e in errors['ErrorItemCollection']])

        self.instance.data = json_response


class BoletoForm(PagamentoFormBase):

    def get_transaction_collection(self, cleaned_data):
        boleto_options = boleto_transaction_options('BRL', 5)

        transaction_collection = [
            boleto_transaction(
                cleaned_data['valor'],
                bank_number=settings.MUNDIPAGG_BOLETO_BANCO,
                document_number='12345678901',
                instructions='Pagar antes do vencimento',
                options=boleto_options
            )
        ]

        return 'boleto_transaction_collection', transaction_collection


class CartaoForm(PagamentoFormBase):
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

    numero_cartao = forms.CharField()
    nome_titular = forms.CharField()
    validade_mes = forms.IntegerField()
    validade_ano = forms.IntegerField()
    verificador = forms.IntegerField()
    bandeira_cartao = forms.ChoiceField(BANDEIRA_CHOICES)

    recorrencia = forms.BooleanField(required=False)

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

    def get_transaction_collection(self, cleaned_data):
        creditcard_transaction_options_data = creditcard_transaction_options(
            payment_method_code=1,
            soft_descriptor_text='Jedi Mega Store',
            currency_iso='BRL',
        )

        creditcard_data = creditcard(
            creditcard_number=cleaned_data['numero_cartao'],
            creditcard_brand=cleaned_data['bandeira_cartao'],
            exp_month=int(cleaned_data['validade_mes']),
            exp_year=int(cleaned_data['validade_ano']),
            security_code=cleaned_data['verificador'],
            holder_name=cleaned_data['nome_titular']
        )

        recurrency_data = None

        if cleaned_data['recorrencia']:
            recurrency_data = recurrency(
                frequency='Monthly',
                interval=1,
                date_to_start_billing=timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                recurrences=0,
                one_dollar_auth=False,
            )

        transaction_collection = [
            creditcard_transaction(
                amount_in_cents=cleaned_data['valor'],
                creditcard=creditcard_data,
                recurrency=recurrency_data,
                options=creditcard_transaction_options_data,
            )
        ]

        return 'creditcard_transaction_collection', transaction_collection
