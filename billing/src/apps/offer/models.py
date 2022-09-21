import uuid

from django.db import models


class SubscriptionCurrency(models.TextChoices):
    RUB = ('RUB', 'Рубль')
    USD = ('USD', 'Доллар')
    EUR = ('EUR', 'Евро')


class SubscriptionType(models.TextChoices):
    ENABLE = ('enable', 'Включена')
    DISABLE = ('disable', 'Выключена')
    ARCHIVE = ('archive', 'Архив')


class Subscription(models.Model):
    """
    Модель подписок
    """

    guid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        verbose_name='Название',
        help_text='Максимальная длина - 255 символов.',
        max_length=255,
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание подписки.',
        blank=True,
        null=True
    )
    type = models.CharField(
        verbose_name='Тип подписки',
        help_text='Необходимо выбрать из представленных.',
        max_length=25,
        choices=SubscriptionType.choices,
        default=SubscriptionType.ENABLE
    )
    price = models.DecimalField(
        verbose_name='Стоимость',
        max_digits=12,
        decimal_places=2
    )
    currency = models.CharField(
        verbose_name='Валюта',
        max_length=3,
        choices=SubscriptionCurrency.choices,
        default=SubscriptionCurrency.RUB
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания.',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата последнего обновления.',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-created_at']

    @classmethod
    def get_object(cls, guid):
        try:
            return cls.objects.get(guid=guid)
        except cls.DoesNotExist:
            return None

    def __str__(self) -> str:
        return f'{self.name}'
