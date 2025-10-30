from django.urls import path
from .views import (
    TransacaoListCreateView,
    TransacaoRetrieveUpdateDestroyView,
    SaldoView,
    adicionar_creditos
)

urlpatterns = [
    path('', TransacaoListCreateView.as_view(), name='transacao-list-create'),
    path('transacoes/<int:idtransacao>/', TransacaoRetrieveUpdateDestroyView.as_view(), name='transacao-detail'),
    path('saldo/', SaldoView.as_view(), name='saldo'),
    path('creditos/adicionar/', adicionar_creditos, name='adicionar-creditos'),  # <-- sem parênteses
]