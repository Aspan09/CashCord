from django.contrib import admin
from .models import CustomUser, CardType, Category, CashbackOffer, BankCards, Bank, Cards


admin.site.register(CustomUser)
admin.site.register(CardType)
admin.site.register(Category)
admin.site.register(CashbackOffer)
admin.site.register(BankCards)
admin.site.register(Bank)
admin.site.register(Cards)
