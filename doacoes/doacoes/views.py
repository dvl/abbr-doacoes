import uuid

from rest_framework import viewsets
from rest_framework.response import Response

# namespaces de merda da MundiPagg
from data_contracts import creditcard, creditcard_transaction, creditcard_transaction_options, create_sale_request, order
from enum_types import PlatformEnvironment, HttpContentTypeEnum
from mundipaggOnePython import GatewayServiceClient

from .serializers import DoacaoSerializer


class DoacaoViewSet(viewsets.ViewSet):

    def create(self, request):
        serializer = DoacaoSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        creditcard_data = creditcard(
            creditcard_number=data['numero_cartao'],
            creditcard_brand=data['bandeira_cartao'],
        )

        return Response({'detail': 'success'})
