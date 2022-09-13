from abc import ABC, abstractmethod


class BillingInterface(ABC):
    """ сюда нужно написать что-нибудь еще))"""
    @abstractmethod
    def create_payment(self) -> None:
        pass
