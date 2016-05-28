from django.conf import settings
from django.utils import timezone

from abbr.doacoes.models import Doacao

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

PERSON_TYPE = {
    Doacao.CPF: 'Person',
    Doacao.CNPJ: 'Company',
}


def _person_type(tipo_documento):
    return PERSON_TYPE[tipo_documento]


def _processar_transacao(dados, transaction_collection):
    buyer_data = buyer(
        name=dados['nome'],
        email=dados['email'],
        document_type=dados['tipo_documento'],
        document_number=dados['numero_documento'],
        person_type=_person_type(dados['tipo_documento']),
    )

    options_request = order(order_reference=dados['id'])

    field, transaction_collection = transaction_collection

    merchant_key = settings.MUNDIPAGG_API_KEY
    end_point = settings.MUNDIPAGG_API_ENDPOINT

    request = create_sale_request(**{
        field: transaction_collection,
        'order': options_request,
        'request_key': merchant_key,
        'buyer': buyer_data,
    })

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

    return json_response


def pagamento_boleto(dados):
    boleto_options = boleto_transaction_options('BRL', 5)

    transaction_collection = [
        boleto_transaction(
            amount_in_cents=int(dados['valor_doacao']) * 100,
            bank_number=settings.MUNDIPAGG_BOLETO_BANCO,
            document_number='12345678909',
            instructions='Pagar antes do vencimento',
            options=boleto_options
        )
    ]

    collection = 'boleto_transaction_collection', transaction_collection

    return _processar_transacao(dados, collection)


def pagamento_cartao(dados, cartao):
    creditcard_transaction_options_data = creditcard_transaction_options(
        payment_method_code=1,
        soft_descriptor_text='ABBR',
        currency_iso='BRL',
    )

    creditcard_data = creditcard(
        creditcard_number=cartao['numero_cartao'],
        creditcard_brand=cartao['bandeira'],
        exp_month=int(cartao['validade_mes']),
        exp_year=int(cartao['validade_ano']),
        security_code=cartao['verificador'],
        holder_name=cartao['nome_titular']
    )

    recurrency_data = None

    if dados['recorrencia']:
        recurrency_data = recurrency(
            frequency='Monthly',
            interval=1,
            date_to_start_billing=timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
            recurrences=0,
            one_dollar_auth=False,
        )

    transaction_collection = [
        creditcard_transaction(
            amount_in_cents=int(dados['valor_doacao']) * 100,
            creditcard=creditcard_data,
            recurrency=recurrency_data,
            options=creditcard_transaction_options_data,
        )
    ]

    collection = 'creditcard_transaction_collection', transaction_collection

    return _processar_transacao(dados, collection)
