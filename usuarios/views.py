import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario, VerificationCode
from .serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
)

# ==========================================================
# 1️⃣ REGISTRO DE USUÁRIO (gera e envia código de verificação)
# ==========================================================
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)  # inativo até verificar

        # gerar código de 6 dígitos
        code = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=10)
        VerificationCode.objects.create(user=user, code=code, expires_at=expires_at)

        # simular envio por SMS
        print(f"📲 Código de verificação para {user.telefone}: {code}")

        # enviar email real (se configurado)
        try:
            send_mail(
                subject="Código de Verificação - Sistema Sinf",
                message=f"Seu código de verificação é: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"❗ Erro ao enviar email: {e}")

        return user

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Usuário criado! Código de verificação enviado."},
            status=status.HTTP_201_CREATED
        )

# ==========================================================
# 2️⃣ LOGIN JWT
# ==========================================================
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ==========================================================
# 3️⃣ PERFIL DO USUÁRIO AUTENTICADO
# ==========================================================
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# ==========================================================
# 4️⃣ VERIFICAÇÃO DO CÓDIGO DE TELEFONE
# ==========================================================
class VerifyPhoneCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        telefone = request.data.get("telefone")
        code = request.data.get("code")

        if not telefone or not code:
            return Response(
                {"error": "Telefone e código são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Usuario.objects.get(telefone=telefone)
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            verification = VerificationCode.objects.filter(
                user=user, code=code
            ).latest("created_at")
        except VerificationCode.DoesNotExist:
            return Response(
                {"error": "Código inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not verification.is_valid():
            return Response(
                {"error": "Código expirado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.telefone_verificado = True
        user.is_active = True
        user.save()

        return Response(
            {"message": "Telefone verificado com sucesso! Agora você pode fazer login."},
            status=status.HTTP_200_OK
        )