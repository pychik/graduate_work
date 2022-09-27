import factory
from apps.offer.models import Subscription, SubscriptionCurrency, SubscriptionType
from apps.transactions.models import Transaction, TransactionStatuses
from django.db import models
from factory import fuzzy


class SubscriptionNames(models.TextChoices):
    bronze = ('bronze', 'bronze')
    silver = ('silver', 'silver')
    gold = ('gold', 'gold')


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription
    guid = factory.Faker('uuid4')
    name = fuzzy.FuzzyChoice(SubscriptionNames.values)
    description = factory.Faker('sentence')
    type = fuzzy.FuzzyChoice(SubscriptionType.choices)
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2,
                          positive=True, min_value=1, max_value=999)
    currency = fuzzy.FuzzyChoice(SubscriptionCurrency.values)


class TransactionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Transaction

    subscription = factory.SubFactory(SubscriptionFactory)
    status = fuzzy.FuzzyChoice(TransactionStatuses.values)
