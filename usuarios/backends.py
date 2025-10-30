from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tenta autenticar por email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # Se não for email, tenta autenticar por telefone
                user = User.objects.get(telefone=username)
            except User.DoesNotExist:
                return None

        # Verifica se a senha é válida
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None