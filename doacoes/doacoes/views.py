from django.conf import settings
from django.utils import crypto, timezone

from rest_framework import viewsets
from rest_framework.response import Response

from mundipagg_one.data_contracts import (
    buyer,
    create_sale_request,
    creditcard,
    creditcard_transaction,
    order,
    recurrency,
)
from mundipagg_one.enum_types import HttpContentType
from mundipagg_one.gateway_service_client import GatewayServiceClient

from .serializers import DoacaoSerializer


class DoacaoViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = DoacaoSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        buyer_data = buyer(
            document_number='12345678901',
            document_type='CPF',
            person_type='Person',
            name=data['nome_titular'],
            email=data['email'],
            email_type='Personal',
        )

        creditcard_data = creditcard(
            creditcard_number=data['numero_cartao'],
            creditcard_brand=data['bandeira_cartao'],
            exp_month=int(data['validade_mes']),
            exp_year=int(data['validade_ano']),
            security_code=data['verificador'],
            holder_name=data['nome_titular'],
        )

        if data['recorrencia']:
            recurrency_data = recurrency(
                frequency='Monthly',
                interval=1,
                date_to_start_billing=timezone.now().strftime("%Y-%m-%dT%H:%M:%S"),
                recurrences=0,
                one_dollar_auth=False,
            )
        else:
            recurrency_data = None

        transaction_collection = [
            creditcard_transaction(
                amount_in_cents=data['valor'],
                creditcard=creditcard_data,
                recurrency=recurrency_data,
            )
        ]

        options_request = order(
            order_reference=crypto.get_random_string(24)
        )

        payment_request = create_sale_request(
            creditcard_transaction_collection=transaction_collection,
            buyer=buyer_data,
            order=options_request
        )

        service_client = GatewayServiceClient(
            settings.MUNDIPAGG_API_KEY,
            settings.MUNDIPAGG_API_ENVIRONMENT,
            HttpContentType.json,
            settings.MUNDIPAGG_API_ENDPOINT,
        )

        http_response = service_client.sale.create_with_request(payment_request)

        return Response(http_response.json(), http_response.status_code)
