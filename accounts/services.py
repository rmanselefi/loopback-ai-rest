from .models import User


class AccountService:
    @staticmethod
    def register_user(validated_data):
        validated_data = dict(validated_data)
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
