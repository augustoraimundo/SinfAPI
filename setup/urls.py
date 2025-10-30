from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({"mensagem": "Bem-vindo a API do Sinf"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/transacoes/', include('transacoes.urls')),
    path('', home),
]
