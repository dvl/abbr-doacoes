from django.views import generic

from . import forms, models


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class PagamentoBaseFormView(generic.CreateView):
    template_name = 'form.html'


class BoletoFormView(PagamentoBaseFormView):
    form_class = forms.BoletoForm


class CartaoFormView(PagamentoBaseFormView):
    form_class = forms.CartaoForm


class SucessoView(generic.DetailView):
    model = models.Transacao
    template_name = 'sucesso.html'
