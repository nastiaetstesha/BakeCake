from django.db import models

# ну тут хз конечно - полет фантазии 
class PromoCode(models.Model):
    PERCENT = 'percent'
    FIXED = 'fixed'
    DISCOUNT_TYPE_CHOICES = [
        (PERCENT, 'Процент'),
        (FIXED, 'Фиксированная сумма'),
    ]

    code = models.CharField('Код', max_length=40, unique=True)
    discount_type = models.CharField(
        'Тип скидки',
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES,
        default=PERCENT
        )
    amount = models.DecimalField(
        'Величина скидки',
        max_digits=8,
        decimal_places=2
        )
    active = models.BooleanField('Активен', default=True)
    valid_from = models.DateTimeField('Действует с', null=True, blank=True)
    valid_until = models.DateTimeField('Действует до', null=True, blank=True)
    max_uses = models.PositiveIntegerField(
        'Максимум применений', null=True, blank=True
        )
    used_count = models.PositiveIntegerField(
        'Сколько раз использовали', default=0
        )

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code
