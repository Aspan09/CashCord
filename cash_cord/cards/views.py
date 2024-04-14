from django.shortcuts import render
from rest_framework import generics, status, viewsets
from .models import CustomUser, CardType, Category, CashbackOffer, BankCards, Bank, Cards
from .serializers import CustomUserSerializer, AuthTokenObtainPairSerializer, SendSerializer, SendIdSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CardsSerializer, CardTypeSerializer, BankSerializer, BankCardsSerializer, \
    CashbackOfferSerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'id': user.id,
            'email': user.email,
            'user_name': user.user_name,
            'sure_name': user.sure_name,
            'address': user.address,
            'phone_number': user.phone_number,
            'user_card_name': user.user_card_name,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        return Response({
            'id': updated_user.id,
            'email': updated_user.email,
            'user_name': updated_user.user_name,
            'sure_name': updated_user.sure_name,
            'address': user.address,
            'phone_number': user.phone_number,
            'user_card_name': user.user_card_name,
        })


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer


class CardTypeList(APIView):

    def get(self, request):
        card_types = CardType.objects.all()
        serializer = CardTypeSerializer(card_types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CardTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCardType(APIView):
    def post(self, request):
        card_type_id = request.data.get('card_type_id')

        try:
            card_type = CardType.objects.get(id=card_type_id)
            card_type.delete()
            return Response({"message": "Тип карты успешно удален"}, status=status.HTTP_204_NO_CONTENT)
        except CardType.DoesNotExist:
            return Response({"error": "Тип карты не найден"}, status=status.HTTP_404_NOT_FOUND)


class BankList(APIView):

    def get(self, request):
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)
        return Response(serializer.data)


class DeleteBank(APIView):
    def post(self, request):
        bank_id = request.data.get('bank_id')

        try:
            bank = Bank.objects.get(id=bank_id)
            bank.delete()
            return Response({"message": "Банк успешно удален"}, status=status.HTTP_204_NO_CONTENT)
        except Bank.DoesNotExist:
            return Response({"error": "Банк не найден"}, status=status.HTTP_404_NOT_FOUND)


class CardsList(APIView):

    def get(self, request):
        cards = Cards.objects.all()
        serializer = CardsSerializer(cards, many=True, context={'request': request})
        data = serializer.data
        filtered_data = [{'id': card['id'], 'card_name': card['card_name'],
                          'card_name_second': card['card_name_second']} for card in data]
        return Response(filtered_data, status=status.HTTP_200_OK)


class DeleteCard(APIView):
    def post(self, request):
        card_id = request.data.get('card_id')

        try:
            card = Cards.objects.get(id=card_id)
            card.delete()
            return Response({"message": "Карта успешно удалена"}, status=status.HTTP_204_NO_CONTENT)
        except Cards.DoesNotExist:
            return Response({"error": "Карта не найдена"}, status=status.HTTP_404_NOT_FOUND)


class CategoryList(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        data = serializer.data
        filtered_data = [{'id': category['id'], 'name_category': category['name_category']} for category in data]
        return Response(filtered_data, status=status.HTTP_200_OK)


class DeleteCategory(APIView):
    def post(self, request):
        category_id = request.data.get('category_id')

        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return Response({"message": "Категория успешно удалена"}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Категория не найдена"}, status=status.HTTP_404_NOT_FOUND)


class AddUserCard(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        card_names = request.data.get('user_card_names', [])  # Get list of card names from JSON data

        # Fetch card instances based on the provided card names
        card_instances = []
        for card_name in card_names:
            try:
                card_instance = Cards.objects.get(card_name=card_name)
                card_instances.append(card_instance)
            except Cards.DoesNotExist:
                return Response({"error": f"Карта '{card_name}' не найдена"}, status=status.HTTP_404_NOT_FOUND)

        # Add each card instance to the user's user_card_name field
        user.user_card_name.add(*card_instances)
        user.save()

        serializer = CustomUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteUserCard(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        card_names = request.data.get('user_card_names', [])  # Get list of card names from JSON data

        # Remove each card instance from the user's user_card_name field
        for card_name in card_names:
            user.user_card_name.filter(card_name=card_name).delete()

        return Response({"message": "Карты успешно удалены"}, status=status.HTTP_204_NO_CONTENT)


class GetCashbackOffers(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendSerializer(data=request.data)
        if serializer.is_valid():
            category_name = serializer.validated_data['category']
            user = request.user

            # Retrieve all cards associated with the user
            user_cards = user.user_card_name.all()
            print(user_cards)
            cashback_offers = []
            # Iterate through each user card to get related cashback offers
            for card in user_cards:
                user_bank = card.bank
                offers = CashbackOffer.objects.filter(name_bank=user_bank, category__name_category=category_name)
                cashback_offers.extend(offers)

            # Sort the cashback offers by cashback percentage in descending order
            sorted_cashback_offers = sorted(cashback_offers, key=lambda x: x.cashback_percentage, reverse=True)

            # Serialize the sorted cashback offers
            serialized_cashback_offers = CashbackOfferSerializer(sorted_cashback_offers, many=True)
            return Response(serialized_cashback_offers.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCardsByBankID(APIView):
    def post(self, request):
        serializer = SendIdSerializer(data=request.data)
        if serializer.is_valid():
            bank_id = serializer.validated_data['bank_id']

            try:
                bank = Bank.objects.get(id=bank_id)
                cards = Cards.objects.filter(bank=bank)
                serializer = CardsSerializer(cards, many=True)
                return Response(serializer.data)
            except Bank.DoesNotExist:
                return Response({"error": "Bank not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

