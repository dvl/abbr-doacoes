from django.core.urlresolvers import reverse_lazy
from django.views import generic

from . import forms


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class BoletoFormView(generic.FormView):
    form_class = forms.BoletoForm
    template_name = 'form.html'
    success_url = reverse_lazy('doacoes:sucesso')


class CartaoFormView(generic.FormView):
    form_class = forms.CartaoForm
    template_name = 'form.html'
    success_url = reverse_lazy('doacoes:sucesso')


class SucessoView(generic.TemplateView):
    template_name = 'sucesso.html'
