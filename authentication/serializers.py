import re
from rest_framework import serializers
from account.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'password2')

        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError('لطفا نام کاربری خود را وارد کنید')
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('این نام کاربری قبلا انتخاب شده است')
        return value

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError('لطفا شماره موبایل خود را وارد کنید')
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("شماره موبایل معتبر ایرانی وارد کنید."
                                              " شماره باید با 09 شروع شده و 11 رقم داشته باشد.")
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('این شماره قبلا ثبت شده است ')
        return value

    def validate(self, data):
        if not data['password'] or not data['password2']:
            raise serializers.ValidationError('لطفا کلمه عبور و تکرار آن را وارد کنید')
        if data['password'] != data['password2']:
            raise serializers.ValidationError('کلمه عبور با تکرار آن مغایرت دارد')
        return data

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create_user(**validated_data)
        return user
