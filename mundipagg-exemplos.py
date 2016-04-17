# -*- coding: utf-8 -*-

import datetime
import uuid

from mundipagg_one.data_contracts import (
    billing_address, boleto_transaction, boleto_transaction_options, buyer,
    buyer_address, create_sale_request, creditcard, creditcard_transaction,
    creditcard_transaction_options, delivery_address, merchant, order,
    request_data, sale_options, shopping_cart, shopping_cart_item
)
from mundipagg_one.enum_types import HttpContentTypeEnum, PlatformEnvironment
from mundipagg_one.gateway_service_client import GatewayServiceClient

# Cria o endereco do comprador
buyer_address_collection_data = [
    buyer_address(
        address_type='Residential',
        city='Tatooine',
        complement='',
        country='Brazil',
        district='Mos Eisley',
        number='123',
        state='RJ',
        street='Mos Eisley Cantina',
        zip_code='20001000')]

# Cria o comprador
buyer_data = buyer(
    address_collection=buyer_address_collection_data,
    birth_date='1990-08-20T00:00:00',
    buyer_category='Normal',
    buyer_reference='C3PO',
    create_date_in_merchant=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    document_number='12345678901',
    document_type='CPF',
    email='lskywalker@r2d2.com',
    email_type='Personal',
    facebook_id='lukeskywalker8917',
    gender='M',
    home_phone='(21)123456789',
    mobile_phone='(21)987654321',
    name='Luke Skywalker',
    person_type='Person',
    twitter_id='@lukeskywalker8917',
    work_phone='(21)28467902')

# Cria o endereco de cobranca
billing_address_data = billing_address(
    city='Tatooine',
    complement='',
    country='Brazil',
    district='Mos Eisley',
    number='123',
    state='RJ',
    street='Mos Eisley Cantina',
    zip_code='20001000')

# Criando a transacao de cartao de credito.
# Coleta os dados do cartão.
creditcard_data = creditcard(billing_address=billing_address_data, creditcard_number='4111111111111111', creditcard_brand='Visa', exp_month=10, exp_year=22,
                             security_code='123', holder_name='LUKE SKYWALKER')

# Cria as opcoes do cartao de credito
creditcard_transaction_options_data = creditcard_transaction_options(
    payment_method_code=1, soft_descriptor_text='Jedi Mega Store', currency_iso='BRL')

# Cria a transação de cartao de credito.
credit_card_transaction_collection_data = [
    creditcard_transaction(
        10000,
        creditcard_data,
        'AuthOnly',
        installment_count=1,
        options=creditcard_transaction_options_data,
        transaction_reference='NumeroDaTransacao')]

# Criando a transacao de boleto
boleto_options = boleto_transaction_options(
    currency_iso='BRL', days_to_add_in_boleto_expiration_date=5)

boleto_transaction_collection_data = [
    boleto_transaction(
        10000,
        bank_number='237',
        document_number='12345678901',
        instructions='Pagar antes do vencimento',
        options=boleto_options,
        billing_address=billing_address_data)]

# Habilita o antiFraud
sale_options_data = sale_options(
    is_anti_fraud_enabled=True,
    anti_fraud_service_code=0,
    retries=1,
    currency_iso_field='BRL')

# Cria o numero do pedido
order_data = order(order_reference='NumeroDoPedido')

# Criando o carrinho de compra
# Cria o endereco de entrega para o carrinho de compras
delivery_address_data = delivery_address(
    city='Galaxy far far away',
    complement='Bridge',
    country='Brazil',
    district='Command Room',
    number='321',
    state='RJ',
    street='Death Star',
    zip_code='10002000')

# Cria a colecao de item do carrinho de compras
shopping_cart_item_collection_data = [
    shopping_cart_item(
        description='Red Lightsaber',
        discount_amount_in_cents=0,
        item_reference='NumeroDoProduto',
        name='Lightsaber',
        quantity=1,
        total_cost_in_cents=18000,
        unit_cost_in_cents=18000)]

# Cria o carrinho de compra
shopping_cart_collection_data = [
    shopping_cart(
        delivery_address=delivery_address_data,
        delivery_deadline=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        estimated_delivery_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        freight_cost_in_cents=2000,
        shipping_company='Empire',
        shopping_cart_item_collection=shopping_cart_item_collection_data)]

# Cria o merchant
merchant_data = merchant(merchant_reference='IdDaLojaPlataforma')

# Cria os dados da requisição
request_data_data = request_data(
    ecommerce_category='B2C',
    ip_address='127.0.0.1',
    origin='SiteDeCompra',
    session_id='IdSesssaoNoSite')

# Cria a requisicao
request = create_sale_request(
    creditcard_transaction_collection=credit_card_transaction_collection_data,
    boleto_transaction_collection=boleto_transaction_collection_data,
    order=order_data,
    buyer=buyer_data,
    shopping_cart_collection=shopping_cart_collection_data,
    options=sale_options_data,
    merchant=merchant_data,
    request_data=request_data_data)

# Coloque sua MerchantKey aqui.
merchant_key = uuid.UUID('85328786-8BA6-420F-9948-5352F5A183EB')
end_point = "https://sandbox.mundipaggone.com"
service_client = GatewayServiceClient(
    merchant_key,
    PlatformEnvironment.sandbox,
    HttpContentTypeEnum.json,
    end_point)

# envia a transação e recebe a resposta do gateway.
http_response = service_client.sale.create_with_request(request)

# Obtem a resposta em json.
json_response = http_response.json()
