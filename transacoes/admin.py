from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = (
        'idtransacao',
        'idordenante',
        'idbeneficiario',
        'tipodeop',
        'categoriadeop',
        'valoracreditar',
        'estado',
        'datadatransacao',
        'prazodatransacao',
    )
    list_filter = ('estado', 'tipodeop', 'categoriadeop')
    search_fields = ('idordenante__username', 'idbeneficiario__username', 'tipodeop', 'categoriadeop')
    readonly_fields = ('datadatransacao',)