from django.conf.urls import url

from abbr.doacoes.views import (
    IndexView, DoacaoView, PagamentoView, SucessoView
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^doar/$', DoacaoView.as_view(), name='inicio'),
    url(r'^pagamento/(?P<pk>[A-Fa-f0-9-]{36})/$', PagamentoView.as_view(), name='pagamento'),
    url(r'^sucesso/(?P<pk>[A-Fa-f0-9-]{36})/$', SucessoView.as_view(), name='sucesso'),
]
