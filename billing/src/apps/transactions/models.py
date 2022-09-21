import uuid

from django.db import models


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
    subscription_guid = models.ForeignKey('offer.Subscription', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Транзакция {self.user_id}: {self.guid}'
