from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, CardType, Category, CashbackOffer, BankCards, Bank, Cards
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'user_name', 'sure_name',
                  'address', 'phone_number', 'user_card_name'
                  ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #     if user:
    #         token['id'] = user.id
    #         token['email'] = user.email
    #         token['user_name'] = user.user_name
    #         token['sure_name'] = user.sure_name
    #         token['address'] = user.address
    #         token['phone_number'] = user.phone_number
    #         # token['user_card_name'] = user.user_card_name
    #     return token
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['user_name'] = self.user.user_name
        data['sure_name'] = self.user.sure_name
        data['address'] = self.user.address
        data['phone_number'] = self.user.phone_number
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class CardTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardType
        fields = '__all__'


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class BankCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCards
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CashbackOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashbackOffer
        fields = '__all__'


class CardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cards
        fields = '__all__'


class SendSerializer(serializers.Serializer):
    category = serializers.CharField()


class SendIdSerializer(serializers.Serializer):
    bank_id = serializers.CharField()


