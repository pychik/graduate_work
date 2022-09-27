import math
import uuid

from apps.offer.models import SubscriptionCurrency
from apps.restapi.errors import NotPaidYetError
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


class TransactionStatuses(models.TextChoices):
    new = ('new', 'новая')
    paid = ('paid', 'оплачена')
    failed = ('failed', 'проваленная')


class Transaction(models.Model):
    """
    Модель транзакции
    """

    guid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.CharField('Id пользователя', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField('Статус', max_length=20,
                              choices=TransactionStatuses.choices,
                              default=TransactionStatuses.new)
    subscription = models.ForeignKey('offer.Subscription', on_delete=models.DO_NOTHING)
    payment_system_id = models.CharField(max_length=50, default='')
    amount = models.DecimalField('Сумма', decimal_places=2, max_digits=10, default=0.0)
    currency = models.CharField(verbose_name='Валюта',
                                max_length=3,
                                choices=SubscriptionCurrency.choices,
                                default=SubscriptionCurrency.RUB
                                )

    def __str__(self):
        return f'Транзакция {self.user_id}: {self.guid}'


class SubscriptionPeriods(models.TextChoices):
    months = ('months', 'months')
    years = ('years', 'years')


class UserSubscriptionStatuses(models.TextChoices):
    active = ('active', 'active')
    expired = ('expired', 'expired')
    payment_waiting = ('payment_waiting', 'payment_waiting')


class UserSubscription(models.Model):
    """
    Модель конкретной подписки юзера
    """
    guid = models.UUIDField(default=uuid.uuid4, primary_key=True,
                            editable=False)  # TODO: Вынести повторяющиеся поля в миксин
    period = models.CharField('Период', max_length=20, choices=SubscriptionPeriods.choices,
                              default=SubscriptionPeriods.months)
    periods_number = models.IntegerField('Количество периодов')
    subscription = models.ForeignKey('offer.Subscription', on_delete=models.DO_NOTHING)
    user_id = models.CharField('Id пользователя', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)  # TODO: Вынести повторяющиеся поля в миксин
    updated_at = models.DateTimeField(auto_now=True)  # TODO: Вынести повторяющиеся поля в миксин
    expires_at = models.DateTimeField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=UserSubscriptionStatuses.choices,
                              default=UserSubscriptionStatuses.payment_waiting)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency = models.CharField(verbose_name='Валюта',
                                max_length=3,
                                choices=SubscriptionCurrency.choices,
                                default=SubscriptionCurrency.RUB
                                )

    transaction = models.OneToOneField(Transaction, on_delete=models.DO_NOTHING, related_name='user_subscription')

    def __str__(self):
        return f'{self.user_id}: {self.subscription.name} : {self.status}'

    def calculate_sub_time(self, start_from=timezone.now(), set_value=False):
        """
        Расчет времени подписки
        """

        sub_time = start_from + relativedelta(**{self.period: self.periods_number})
        if set_value:
            self.expires_at = sub_time
            self.save()
        return sub_time

    def calculate_amount(self, set_value):
        if self.period == SubscriptionPeriods.months:
            amount = self.periods_number * self.subscription.price
        else:
            amount = self.periods_number * self.subscription.price * 12
        if set_value:
            self.amount = amount
        return amount

    def calculate_refund_amount(self):
        """
        Метод расчета суммы возврата,
        пропорционально оставшемуся времени подписки
        Так же вводим grace_period, в течение которого можно вернуть деньги полностью
        """
        if not self.paid_at:
            raise NotPaidYetError
        time_passed = timezone.now() - self.paid_at
        grace_period = timezone.timedelta(**settings.REFUND_GRACE_PERIOD)
        if grace_period <= time_passed:
            # вернем полную стоимость
            return self.amount

        full_amount = self.expires_at - self.paid_at
        time_left = self.expires_at - timezone.now()
        left = time_left / full_amount
        to_refund = math.ceil(float(self.amount) * left)
        return to_refund


class RefundStatuses(models.TextChoices):
    succeeded = ('succeeded', 'succeeded')
    canceled = ('canceled', 'canceled')


class Refund(models.Model):
    """
    Модель возврата платежа
    """
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING, related_name='refunds')
    status = models.CharField(max_length=20, choices=RefundStatuses.choices, default='')
    cancellation_details = models.JSONField(default=None, null=True)
    payment_system_id = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    currency = models.CharField(verbose_name='Валюта',
                                max_length=3,
                                choices=SubscriptionCurrency.choices,
                                default=SubscriptionCurrency.RUB
                                )
