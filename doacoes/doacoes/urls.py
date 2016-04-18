from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cartao/$', views.CartaoFormView.as_view(), name='cartao'),
    url(r'^boleto/$', views.BoletoFormView.as_view(), name='boleto'),
    url(r'^sucesso/$', views.SucessoView.as_view(), name='sucesso'),
]
