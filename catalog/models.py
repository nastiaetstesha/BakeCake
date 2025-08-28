from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


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


class Cake(models.Model):
    title = models.CharField('Название торта', max_length=120)
    slug = models.SlugField('Слаг', max_length=140, unique=True)
    short_description = models.CharField('Короткое описание', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)

    image = models.ImageField('Главная картинка', upload_to='cakes/')
    base_price = models.DecimalField('Базовая цена, ₽',
                                     max_digits=10,
                                     decimal_places=2,
                                     validators=[MinValueValidator(Decimal('0.00'))])
    weight_grams = models.PositiveIntegerField(
        'Вес, г', validators=[MinValueValidator(1)]
        )
    servings = models.PositiveIntegerField('Порций', null=True, blank=True)
    diameter_cm = models.PositiveIntegerField('Диаметр, см', null=True, blank=True)

    # Кастомизация
    allow_inscription = models.BooleanField('Разрешить надпись', default=True)
    inscription_extra_price = models.DecimalField('Доплата за надпись, ₽', max_digits=8, decimal_places=2,
                                                  default=Decimal('0.00'),
                                                  validators=[MinValueValidator(Decimal('0.00'))])

    # Доступные начинки для этого торта (категория options: filling)
    available_fillings = models.ManyToManyField(
        Option, blank=True, related_name='cakes_with_filling',
        limit_choices_to={'category__slug': 'filling'}, verbose_name='Доступные начинки'
    )

    # Оценка сроков приготовления (для «когда приедет»)
    prep_time_min_hours = models.PositiveSmallIntegerField('Подготовка, мин. часов', default=24)
    prep_time_max_hours = models.PositiveSmallIntegerField('Подготовка, макс. часов', default=48)

    is_active = models.BooleanField('Опубликован', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Торт (базовый)'
        verbose_name_plural = 'Торты (базовые)'
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def from_price(self) -> Decimal:
        """Цена 'от': базовая без учёта кастомизаций."""
        return self.base_price


class CakeImage(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE, related_name='gallery', verbose_name='Торт')
    image = models.ImageField('Изображение', upload_to='cakes/')
    alt_text = models.CharField('Alt-текст', max_length=120, blank=True)
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Фото торта'
        verbose_name_plural = 'Фото тортов'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'Фото {self.cake} #{self.id}'