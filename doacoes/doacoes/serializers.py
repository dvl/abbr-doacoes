from django.utils import timezone

from rest_framework import serializers

from .models import Bandeira


class DoacaoSerializer(serializers.Serializer):
    email = serializers.EmailField()

    numero_cartao = serializers.CharField()
    nome_titular = serializers.CharField()
    validade_mes = serializers.IntegerField()
    validade_ano = serializers.IntegerField()
    verificador = serializers.IntegerField()
    bandeira_cartao = serializers.ChoiceField(Bandeira.choices())

    valor = serializers.IntegerField()
    recorrencia = serializers.BooleanField()

    def validate_validade_mes(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError('Insira um mês válido.')

        return value

    def validate_validade_ano(self, value):
        if value < timezone.now().year or len(str(value)) != 4:
            raise serializers.ValidationError('Insira um ano válido.')

        return value

    def validate_verificador(self, value):
        if len(str(value)) not in [3, 4]:
            raise serializers.ValidationError('Insira um verificador válido.')

        return value
