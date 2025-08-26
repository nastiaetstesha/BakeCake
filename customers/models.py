from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='customer',
        verbose_name='Пользователь'
    )
    phone = models.CharField('Телефон', max_length=32, blank=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        if self.user:
            return self.user.get_username()
        return f'Customer #{self.id}'


class Address(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name='Клиент'
    )
    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=100)
    house = models.CharField('Дом', max_length=30)
    apartment = models.CharField('Квартира', max_length=30, blank=True)
    comment = models.CharField(
        'Комментарий к адресу', max_length=200, blank=True
        )
    is_default = models.BooleanField('Адрес по умолчанию', default=False)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.city}, {self.street} {self.house}'
