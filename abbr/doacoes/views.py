import xmltodict

from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from abbr.core.mundipagg import pagamento_boleto, pagamento_cartao
from abbr.doacoes.forms import DoacaoForm, PagamentoForm
from abbr.doacoes.models import Doacao


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class DoacaoView(generic.CreateView):
    form_class = DoacaoForm
    template_name = 'base_form.html'

    def get_initial(self):
        return {
            'forma_pagamento': self.kwargs['forma_pagamento'],
        }

    def get_form(self, form_class=None):
        form_class = super().get_form(form_class)

        if self.kwargs['forma_pagamento'] != Doacao.CARTAO_CREDITO:
            del form_class.fields['recorrencia']

        return form_class

    def get_success_url(self):
        return reverse_lazy('doacoes:pagamento', kwargs={'pk': self.object.pk})


class PagamentoView(generic.UpdateView):
    form_class = PagamentoForm
    model = Doacao
    template_name = 'pagamento_form.html'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(resposta_gateway__isnull=True)  # Tudo que ainda não foi finalizado

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.forma_pagamento == Doacao.CARTAO_CREDITO:
            return self.render_to_response(self.get_context_data())

        if self.object.forma_pagamento == Doacao.BOLETO_BANCARIO:
            # vai direto para MundiPagg, os dados que já tenho em
            # self.object já são o bastante para gerar um boleto
            # bancário.
            self.object.resposta_gateway = pagamento_boleto(self.object.__dict__)
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        resposta = pagamento_cartao(self.object.__dict__, form.cleaned_data)

        erros = resposta.get('ErrorReport')

        if erros:
            # por que essa bizarrice? não tem nada demais só estamos
            # reaproveitando o validador e o comportamento e o comportamento
            # do form_invalid que fazem exatamente o que eu quero, mesmo
            # que pareça feio.
            #
            # Pior que isso seria efetuar um pagamento dentro da validação
            # do form, sem o escopo do request.
            erros = [e['Description'] for e in erros['ErrorItemCollection']]
            form.add_error(None, erros)

            return self.form_invalid(form)

        self.object.resposta_gateway = resposta
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('doacoes:sucesso', kwargs={'pk': self.object.pk})


class SucessoView(generic.DetailView):
    model = Doacao
    template_name = 'sucesso.html'


@csrf_exempt
@require_http_methods(['POST'])
def webhook_mundipagg(request):
    # essa porra é orgão público para em pleno ano de 2016 usar XML?
    # xml = request.body
    # o formato abaixo é tão bosta que o POSTMAN não sabe enviar um XML assim...
    try:
        xml = request.POST['xmlStatusNotification']
    except KeyError:
        return HttpResponse(status=412)

    try:
        better_data_structure_than_xml = xmltodict.parse(xml)
    except:
        # Sim, sem especificar, o XML da MundiPagg não é NEM UM POUCO CONFIÁVEL
        return HttpResponse(status=400)

    reference = better_data_structure_than_xml['StatusNotification']['OrderReference']

    doacao = Doacao.objects.get(pk=reference)
    doacao.notificacao_gateway = better_data_structure_than_xml
    doacao.save()

    return JsonResponse({'recebido': True})


def webhook_paypal(request):
    pass
