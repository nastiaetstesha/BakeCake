from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from customers.models import Customer
from promos.models import PromoCode
from catalog.models import Option, Cake


class Order(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PAID = 'paid', 'Оплачен'
        PREPARING = 'preparing', 'Готовится'
        ON_DELIVERY = 'on_delivery', 'Доставляется'
        DELIVERED = 'delivered', 'Доставлен'
        CANCELLED = 'cancelled', 'Отменён'

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Клиент'
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=Status.choices,
        # черновик
        default=Status.PAID
        )

    # Контакты и адреса доставки
    contact_name = models.CharField('Имя получателя', max_length=100)
    phone = models.CharField('Телефон', max_length=32)
    email = models.EmailField('Email', blank=True)

    city = models.CharField('Город', max_length=100)
    street = models.CharField('Улица', max_length=100)
    house = models.CharField('Дом', max_length=30)
    apartment = models.CharField('Квартира', max_length=30, blank=True)
    delivery_comment = models.CharField(
        'Комментарий к доставке', max_length=500, blank=True
        )
    delivery_date = models.DateField('Дата доставки')

    consent_personal_data = models.BooleanField(
        'Согласие на обработку ПД',
        default=False
        )

    # UTM для маркетинга - наверное надо
    # Мы считываем UTM из URL (например, с посадочной страницы),
    # кладём в сессию и при оформлении заказа записываем в поля заказа.
    # Потом строить отчёты: количество/выручка по каналам и кампаниям.
    utm_source = models.CharField('utm_source', max_length=80, blank=True)
    utm_medium = models.CharField('utm_medium', max_length=80, blank=True)
    utm_campaign = models.CharField('utm_campaign', max_length=120, blank=True)

    # Промокод
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Промокод'
        )

    # Денежные поля
    subtotal = models.DecimalField('Сумма позиций', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_total = models.DecimalField('Скидка', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField('Стоимость доставки', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    rush_fee = models.DecimalField('Срочность (в 24ч)', max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField('Итого к оплате', max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                validators=[MinValueValidator(0)])

    def calc_discount(self, subtotal: Decimal) -> Decimal:
        if not self.promo_code or not self.promo_code.active:
            return Decimal('0.00')
        if self.promo_code.discount_type == PromoCode.PERCENT:
            return subtotal * (self.promo_code.amount / Decimal('100'))
        return min(self.promo_code.amount, subtotal)

    def recalc_totals(self, save: bool = True):
        for item in self.items.all():
            item.recalc_subtotal(save=False)

        subtotal = sum((i.line_subtotal for i in self.items.all()), Decimal('0.00'))
        discount = self.calc_discount(subtotal)
        total = subtotal - discount + (self.delivery_fee or 0) + (self.rush_fee or 0)
        if total < 0:
            total = Decimal('0.00')

        self.subtotal = subtotal
        self.discount_total = discount
        self.total = total
        if save:
            self.save(update_fields=['subtotal', 'discount_total', 'total'])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} ({self.status})'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
        )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Базовый торт',
        null=True,   # временно - бд поломалась 
        blank=True
    )

    # Одиночные опции (limit_choices_to по slug категории)
    levels = models.ForeignKey(
        # Пример: нельзя удалить опцию “Карамельный топпинг”, если она есть в каких-то заказах
        Option, on_delete=models.PROTECT, null=True, blank=True, related_name='level_items',
        limit_choices_to={'category__slug': 'levels'}, verbose_name='Уровни'
    )
    shape = models.ForeignKey(
        Option, on_delete=models.PROTECT, null=True, blank=True, related_name='shape_items',
        limit_choices_to={'category__slug': 'shape'}, verbose_name='Форма'
    )
    topping = models.ForeignKey(
        Option, on_delete=models.PROTECT, null=True, blank=True, related_name='topping_items',
        limit_choices_to={'category__slug': 'topping'}, verbose_name='Топпинг'
    )

    # Надпись
    inscription_text = models.CharField(
        'Надпись (необязательно)',
        max_length=64,
        blank=True,
        help_text='Мы можем разместить на торте любую надпись, например: «С днём рождения!»'
    )
    inscription_price = models.DecimalField(
        'Цена надписи, ₽',
        max_digits=8, decimal_places=2,
        default=Decimal('500.00')
    )
    # Мультивыбор? опций — ягоды и декор через through, чтобы фиксировать цену на момент покупки
    # berries = models.ManyToManyField(
    #     Option, through='OrderItemBerry', related_name='berry_items', blank=True, verbose_name='Ягоды'
    # )
    # decors = models.ManyToManyField(
    #     Option, through='OrderItemDecor', related_name='decor_items', blank=True, verbose_name='Декор'
    # )
    berry = models.ForeignKey(
        Option, on_delete=models.PROTECT, null=True, blank=True, related_name='berry_item',
        limit_choices_to={'category__slug': 'berries'}, verbose_name='Ягоды'
    )
    decor = models.ForeignKey(
        Option, on_delete=models.PROTECT, null=True, blank=True, related_name='decor_item',
        limit_choices_to={'category__slug': 'decor'}, verbose_name='Декор'
    )
    # Денежные поля по позиции
    base_price = models.DecimalField(
        'Базовая цена торта, ₽', max_digits=10, decimal_places=2,
        default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))]
    )
    line_subtotal = models.DecimalField(
        'Сумма по позиции, ₽', max_digits=10, decimal_places=2,
        default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))]
    )

    def _delta(self, opt: Option | None) -> Decimal:
        return (opt.price_delta if opt else Decimal('0.00')) or Decimal('0.00')

    def recalc_subtotal(self, save: bool = True) -> Decimal:
        if (self.base_price is None or self.base_price == Decimal('0.00')) and self.cake:
            self.base_price = self.cake.base_price or Decimal('0.00')

        total = (self.base_price or Decimal('0.00'))
        total += self._delta(self.levels) + self._delta(self.shape) + self._delta(self.topping)
        total += self._delta(self.berry) + self._delta(self.decor)

        if (self.inscription_text or '').strip():
            total += self.inscription_price or Decimal('0.00')

        if total < 0:
            total = Decimal('0.00')

        self.line_subtotal = total
        if save:
            super(OrderItem, self).save(update_fields=['base_price', 'line_subtotal', 'inscription_price'])
        return self.line_subtotal

    def save(self, *args, **kwargs):
        if not (self.inscription_text or '').strip():
            self.inscription_price = Decimal('0.00')
        result = super().save(*args, **kwargs)
        self.recalc_subtotal(save=True)
        self.order.recalc_totals(save=True)
        return result

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'Item #{self.id} of Order #{self.order_id}'


# class OrderItemBerry(models.Model):
#     item = models.ForeignKey(
#         OrderItem,
#         on_delete=models.CASCADE,
#         related_name='berry_links',
#         verbose_name='Позиция'
#         )
#     option = models.ForeignKey(
#         Option, on_delete=models.PROTECT, related_name='as_berry',
#         limit_choices_to={'category__slug': 'berries'}, verbose_name='Опция (ягода)'
#     )
#     price_at_purchase = models.DecimalField(
#         'Цена ягоды при покупке',
#         max_digits=15,
#         decimal_places=2
#         )

#     def save(self, *args, **kwargs):
#         if not self.price_at_purchase or self.price_at_purchase == Decimal('0.00'):
#             self.price_at_purchase = self.option.price_delta or Decimal('0.00')
#         super().save(*args, **kwargs)
#         self.item.recalc_subtotal(save=True)
#         self.item.order.recalc_totals(save=True)

#     class Meta:
#         verbose_name = 'Ягода в позиции'
#         verbose_name_plural = 'Ягоды в позиции'
#         unique_together = ('item', 'option')


# class OrderItemDecor(models.Model):
#     item = models.ForeignKey(
#         OrderItem,
#         on_delete=models.CASCADE,
#         related_name='decor_links',
#         verbose_name='Позиция'
#         )
#     option = models.ForeignKey(
#         Option, on_delete=models.PROTECT, related_name='as_decor',
#         limit_choices_to={'category__slug': 'decor'}, verbose_name='Опция (декор)'
#     )
#     # нужно ли это?
#     price_at_purchase = models.DecimalField(
#         'Цена декора при покупке',
#         max_digits=8,
#         decimal_places=2
#         )

#     def save(self, *args, **kwargs):
#         if not self.price_at_purchase or self.price_at_purchase == Decimal('0.00'):
#             self.price_at_purchase = self.option.price_delta or Decimal('0.00')
#         super().save(*args, **kwargs)
#         self.item.recalc_subtotal(save=True)
#         self.item.order.recalc_totals(save=True)

#     class Meta:
#         verbose_name = 'Декор в позиции'
#         verbose_name_plural = 'Декор в позиции'
#         unique_together = ('item', 'option')
