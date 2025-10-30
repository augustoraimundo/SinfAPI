from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from decimal import Decimal
from .models import Transacao
from .serializers import TransacaoSerializer


# ----- Views de transações -----
class TransacaoListCreateView(generics.ListCreateAPIView):
    serializer_class = TransacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Transacao.objects.filter(idordenante=self.request.user)
        beneficiario = self.request.query_params.get('beneficiario')
        if beneficiario:
            queryset = queryset.filter(idbeneficiario__id=beneficiario)
        return queryset

    def perform_create(self, serializer):
        transacao = serializer.save(idordenante=self.request.user)
        try:
            transacao.concluir()  # Tenta concluir automaticamente
        except ValueError:
            pass  # Mantém como pendente se saldo insuficiente


class TransacaoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'idtransacao'

    def get_queryset(self):
        return Transacao.objects.filter(idordenante=self.request.user)


# ----- View para consultar saldo -----
class SaldoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "usuario": request.user.username,
            "saldo": request.user.saldo
        })


# ----- Endpoint opcional para adicionar créditos -----
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def adicionar_creditos(request):
    """
    Adiciona créditos ao saldo do usuário logado.
    Exemplo de payload: { "valor": 100.50 }
    """
    valor = request.data.get('valor')

    if valor is None:
        return Response({"error": "Informe o valor a adicionar."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        valor_decimal = Decimal(valor)
    except:
        return Response({"error": "Valor inválido."}, status=status.HTTP_400_BAD_REQUEST)

    if valor_decimal <= 0:
        return Response({"error": "O valor deve ser maior que zero."}, status=status.HTTP_400_BAD_REQUEST)

    usuario = request.user
    usuario.saldo += valor_decimal
    usuario.save()

    return Response({
        "usuario": usuario.username,
        "novo_saldo": usuario.saldo
    }, status=status.HTTP_200_OK)