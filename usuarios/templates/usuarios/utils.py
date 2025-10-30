import random
from datetime import datetime, timedelta
from .models import VerificationCode

def send_verification_code(user):
    # Gera um código aleatório de 6 dígitos
    code = str(random.randint(100000, 999999))

    # Define validade de 5 minutos
    expires_at = datetime.now() + timedelta(minutes=5)

    # Cria o registro no banco
    VerificationCode.objects.create(user=user, code=code, expires_at=expires_at)

    # Simula envio por SMS (aqui podes integrar Twilio no futuro)
    print(f"📱 Código de verificação para {user.telefone}: {code}")

    return code