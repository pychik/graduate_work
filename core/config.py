from pydantic import BaseSettings


class BillingSet(BaseSettings):
    YOOKASSA_ID: str = ...
    YOOKASSA_API_SECRET: str = ...

    # TEST_MASTERCARD_1: int = 5555555555554477
    # TEST_MASTERCARD_2: int = 5555555555554444
    # TEST_MAESTRO: int = 6759649826438453
    # TEST_VISA: int = 4793128161644804

    REDIRECT_URL: str = "http://127.0.0.1:7777"

    class Config:
        env_file = '.env'
        case_sensitive = False


settings = BillingSet()
