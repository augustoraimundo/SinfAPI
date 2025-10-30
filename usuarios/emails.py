from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

def enviar_email_ativacao(request, user):
    dominio = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link_ativacao = f"http://{dominio}/api/usuarios/ativar-email/{uid}/{token}/"

    assunto = "Ative sua conta - Sistema Sinf"
    mensagem = render_to_string('usuarios/email_ativacao.html', {
        'user': user,
        'link': link_ativacao,
    })

    send_mail(
        assunto,
        mensagem,
        'no-reply@sinf.com',
        [user.email],
        fail_silently=False,
    )