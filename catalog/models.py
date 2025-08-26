from django.db import models


class OptionCategory(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    slug = models.SlugField('Слаг',
                            max_length=60,
                            unique=True,
                            help_text='Например: levels, shape, topping, berries, decor')
    multi_select = models.BooleanField('Множественный выбор', default=False)

    class Meta:
        verbose_name = 'Категория опций'
        verbose_name_plural = 'Категории опций'

    def __str__(self):
        return self.name


class Option(models.Model):
    category = models.ForeignKey(
        OptionCategory,
        on_delete=models.PROTECT,  # PROTECT — нельзя удалить категорию, если есть опции
        related_name='options',
        verbose_name='Категория'
    )
    name = models.CharField('Название опции', max_length=100)
    price_delta = models.DecimalField(
        'Надбавка к цене',
        max_digits=8,
        decimal_places=2,
        default=0
        )
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        unique_together = ('category', 'name')
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'

    def __str__(self):
        return f'{self.category.slug}: {self.name} (+{self.price_delta})'
