from rest_framework import serializers
from .models import Transacao

class TransacaoSerializer(serializers.ModelSerializer):
    datadatransacao = serializers.DateTimeField(read_only=True)
    estado = serializers.CharField(read_only=True)
    idordenante = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transacao
        fields = [
            'idtransacao', 'idordenante', 'idbeneficiario', 'estado',
            'valoracreditar', 'tipodeop', 'categoriadeop',
            'notasdatransacao', 'datadatransacao', 'prazodatransacao', 'pin'
        ]

    def create(self, validated_data):
        # O idordenante será atribuído automaticamente na view
        return Transacao.objects.create(**validated_data)