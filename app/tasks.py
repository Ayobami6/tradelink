from celery import shared_task
from utils.mails import sendmail
import traceback
import logging


logger = logging.getLogger(__name__)


@shared_task
def update_exchange_rates() -> None:
    from app.models import ExchangeRate
    from utils.utils import get_exchange_rate

    rates = get_exchange_rate()
    for currency_code, rate in rates.items():
        ExchangeRate.objects.update_or_create(
            currency_code=currency_code, defaults={"rate": rate}
        )


@shared_task
def send_email_async(username: str, message: str, email: str, subject: str) -> None:
    """Send email asynchronously celery"""
    try:
        sendmail(subject, message, email, username)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"An exception occurred: {e}")
