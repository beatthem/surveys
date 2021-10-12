from rest_framework import serializers
from users.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('username', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'Нужна электронная почта для входа.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Нужен пароль для входа.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Нет пользователя с данной почтой и паролем'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Данный пользователь не активен.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }