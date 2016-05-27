from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic

from abbr.core.mundipagg import boleto_bancario, cartao_credito
from abbr.doacoes.forms import DoacaoForm, PagamentoForm
from abbr.doacoes.models import Doacao


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class DoacaoView(generic.CreateView):
    form_class = DoacaoForm
    template_name = 'form.html'

    def get_initial(self):
        return {
            'forma_pagamento': self.kwargs.get('forma_pagamento'),
        }

    def get_form(self, form_class=None):
        form_class = super().get_form(form_class)

        if self.request.GET.get('forma_pagamento') != Doacao.CARTAO_CREDITO:
            del form_class.fields['recorrencia']

        return form_class

    def get_success_url(self):
        return reverse_lazy('doacoes:pagamento', kwargs={'pk': self.object.pk})


class PagamentoView(generic.UpdateView):
    form_class = PagamentoForm
    model = Doacao
    template_name = 'form.html'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(resposta_gateway__isnull=True)  # Tudo que ainda não foi pago

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.forma_pagamento in Doacao.CARTAO_CREDITO:
            return self.render_to_response(self.get_context_data())

        if self.object.forma_pagamento in Doacao.BOLETO_BANCARIO:
            # vai direto para MundiPagg, os dados que já tenho em
            # self.object já são o bastante para gerar um boleto
            # bancário.
            self.object.resposta_gateway = boleto_bancario(self.object)
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        resposta = cartao_credito(self.object, form)

        if resposta['sucesso'] is False:
            # injeta o erros no form de alguma forma...
            # por que essa bizarrice? não tem nada demais só estamos
            # reaproveitando o validador e o comportamento e o comportamento
            # do form_invalid que fazem exatamente o que eu quero, mesmo
            # que pareça feio.
            #
            # Pior que isso seria efetuar um pagamento dentro da validação
            # do form, sem o escopo do request.
            return self.form_invalid(form)

        self.object.resposta_gateway = resposta
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('doacoes:sucesso', kwargs={'pk': self.object.pk})


class SucessoView(generic.DetailView):
    model = Doacao
    template_name = 'sucesso.html'


def webhook_mundipagg(request):
    pass


def webhook_paypal(request):
    pass
