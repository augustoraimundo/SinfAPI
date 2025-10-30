from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()  # Usa o modelo customizado com telefone


# 🔹 Serializer para Registrar Usuário
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'telefone', 'password', 'password2']
        extra_kwargs = {
            'email': {'required': True},
            'telefone': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# 🔹 Serializer customizado para o Token JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adiciona informações extras no token
        token['username'] = user.username
        token['email'] = user.email
        token['telefone'] = user.telefone
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Inclui também os dados do usuário na resposta (útil para o Flutter)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'telefone': self.user.telefone,
        }
        return data


# 🔹 Serializer do Perfil do Usuário autenticado
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'telefone', 'first_name', 'last_name']

class VerificarTelefoneSerializer(serializers.Serializer):
    telefone = serializers.CharField(required=True)
    codigo = serializers.CharField(required=True)