from django.conf.urls import url

from abbr.doacoes.views import (
    IndexView, DoacaoView, PagamentoView, SucessoView,
    webhook_mundipagg, webhook_paypal
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^doar/(?P<forma_pagamento>boleto|cartao|paypal)/$', DoacaoView.as_view(), name='inicio'),
    url(r'^pagamento/(?P<pk>[A-Fa-f0-9-]{36})/$', PagamentoView.as_view(), name='pagamento'),
    url(r'^sucesso/(?P<pk>[A-Fa-f0-9-]{36})/$', SucessoView.as_view(), name='sucesso'),

    url(r'^webhooks/mundipagg/$', webhook_mundipagg, name='webhook-mundipagg'),
    url(r'^webhooks/paypal/$', webhook_paypal, name='webhook-paypal'),

]
