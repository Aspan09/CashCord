from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CardType(models.Model):
    card_type = models.CharField(verbose_name='Тип карты', max_length=255)

    def __str__(self):
        return self.card_type

    class Meta:
        verbose_name = "Тип карты"
        verbose_name_plural = "Типы карт"


class Bank(models.Model):
    bank_name = models.CharField(verbose_name='Имя банка', max_length=255)

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name = "Имя банка"
        verbose_name_plural = "Имена банков"


class Cards(models.Model):
    bank = models.ForeignKey(Bank, verbose_name='Банк', on_delete=models.CASCADE)
    card_name = models.CharField(verbose_name='Основная карты', max_length=255)
    card_name_second = models.CharField(verbose_name='Дополнительная карта', max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.bank} - {self.card_name} - {self.card_name_second}% Cashback"

    class Meta:
        verbose_name = "Имя карты"
        verbose_name_plural = "Имена карт"


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    user_name = models.CharField(verbose_name='Имя пользователя', max_length=255)
    sure_name = models.CharField(verbose_name='Фамилия пользователя', max_length=255)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255)

    user_card_name = models.ManyToManyField(Cards, verbose_name='Название карты', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Дата создания аккаунта", auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class BankCards(models.Model):

    name_bank = models.ForeignKey(Bank, verbose_name='Название Банка', on_delete=models.CASCADE)
    card_type = models.ForeignKey(CardType, verbose_name='Тип карты', on_delete=models.CASCADE)
    card_number = models.CharField(verbose_name='Название карты', max_length=255)
    expiry_date = models.DateField(verbose_name='Срок действия до')
    user_id = models.ForeignKey(CustomUser, verbose_name='ID владельца карты', on_delete=models.CASCADE)

    def __str__(self):
        return self.name_bank

    class Meta:
        verbose_name = "Карта банка"
        verbose_name_plural = "Карты банка"


class Category(models.Model):

    name_category = models.CharField(verbose_name='Название категории', max_length=255)

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class CashbackOffer(models.Model):
    CARD_CHOICES = (
        ('Jusan Bank', 'Jusan Bank'),
        ('Simply', 'Simply'),
        ('CenterCredit Bank', 'CenterCredit Bank'),
        ('Bereke Bank', 'Bereke Bank'),
        ('Forte Bank', 'Forte Bank'),
        ('Halyk Bank', 'Halyk Bank'),
        ('Kaspi Bank', 'Kaspi Bank'),
        ('Eurasian Bank', 'Eurasian Bank'),
        ('RBK', 'RBK'),
        ('Home Credit Bank', 'Home Credit Bank')
    )
    name_bank = models.CharField(verbose_name='Название Банка', choices=CARD_CHOICES)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    cashback_percentage = models.DecimalField(verbose_name='Процент Кэшбэка', max_digits=5, decimal_places=2, blank=True, null=True)
    conditions = models.TextField(verbose_name='Условия', blank=True, null=True)
    expiry_date = models.DateField(verbose_name='Срок Действия')
    restrictions = models.TextField(verbose_name='Ограничения', blank=True, null=True)

    def __str__(self):
        return f"{self.name_bank} - {self.category} - {self.cashback_percentage}% Cashback"

    class Meta:
        verbose_name = "Предложение по кэшбэку"
        verbose_name_plural = "Предложения по кэшбэку"

