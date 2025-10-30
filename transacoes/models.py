from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import transaction as db_transaction
from decimal import Decimal

class Transacao(models.Model):
    ESTADO_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Concluída', 'Concluída'),
        ('Cancelada', 'Cancelada'),
    ]

    TIPO_DE_OP_CHOICES = [
        ('Pronto Pagamento', 'Pronto Pagamento'),
        ('Transação de Crédito', 'Transação de Crédito'),
    ]

    CATEGORIA_CHOICES = [
        ('Contribuição', 'Contribuição'),
        ('Empréstimo', 'Empréstimo'),
        ('Kixikila', 'Kixikila'),
        ('Oferta', 'Oferta'),
        ('Compra', 'Compra'),
        ('Salário', 'Salário'),
    ]

    idtransacao = models.AutoField(primary_key=True)
    idordenante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transacoes_feitas'
    )
    idbeneficiario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transacoes_recebidas'
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendente')
    valoracreditar = models.DecimalField(max_digits=12, decimal_places=2)
    tipodeop = models.CharField(max_length=50, choices=TIPO_DE_OP_CHOICES)
    categoriadeop = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='Contribuição')
    notasdatransacao = models.TextField(blank=True, null=True)
    datadatransacao = models.DateTimeField(default=timezone.now)
    prazodatransacao = models.CharField(max_length=50, default='Sem Data')
    pin = models.CharField(max_length=10, default='0')

    def __str__(self):
        return f"{self.idtransacao} - {self.tipodeop} - {self.valoracreditar}"

    def concluir(self):
        """
        Conclui a transação, subtraindo saldo do ordenante
        e adicionando ao beneficiário, apenas se houver saldo suficiente.
        """
        if self.estado != 'Concluída':
            with db_transaction.atomic():
                if self.idordenante.saldo < self.valoracreditar:
                    raise ValueError("Saldo insuficiente para concluir a transação.")

                # Atualiza saldos
                self.idordenante.saldo -= self.valoracreditar
                self.idordenante.save()
                self.idbeneficiario.saldo += self.valoracreditar
                self.idbeneficiario.save()

                # Atualiza estado da transação
                self.estado = 'Concluída'
                self.save()