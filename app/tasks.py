from celery import shared_task


@shared_task
def update_exchange_rates() -> None:
    from app.models import ExchangeRate
    from utils.utils import get_exchange_rate

    rates = get_exchange_rate()
    for currency_code, rate in rates.items():
        ExchangeRate.objects.update_or_create(
            currency_code=currency_code, defaults={"rate": rate}
        )
