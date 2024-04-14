from django.urls import include, path

from .views import RegisterUserView, AuthTokenObtainPairView, CardTypeList, BankList, \
    CardsList, CategoryList, AddUserCard, GetCashbackOffers, GetCardsByBankID, DeleteUserCard, DeleteCardType, \
    DeleteBank, DeleteCard, DeleteCategory

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/auth/', AuthTokenObtainPairView.as_view(), name='login'),
    path('api/user_card/', AddUserCard.as_view(), name='user_card'),
    path('api/card_type/', CardTypeList.as_view(), name='card_type'),
    path('api/banks/', BankList.as_view(), name='banks'),
    path('api/cards/', CardsList.as_view(), name='cards'),
    path('api/categories/', CategoryList.as_view(), name='category'),
    path('get_cashback_offers/', GetCashbackOffers.as_view(), name='get_cashback_offers'),
    path('get_card_by_bank_id/', GetCardsByBankID.as_view(), name='get_card_by_bank_id'),

    # delete API
    path('delete_card_type/', DeleteCardType.as_view(), name='delete_card_type'),
    path('delete_bank/', DeleteBank.as_view(), name='delete_bank'),
    path('delete_card/', DeleteCard.as_view(), name='delete_card'),
    path('delete_category/', DeleteCategory.as_view(), name='delete_category'),
    path('delete_user_card/', DeleteUserCard.as_view(), name='delete_user_card'),

]

