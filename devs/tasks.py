from celery import shared_task


@shared_task
def log_ip_country(ip_address: str, country: str) -> None:
    from devs.models import IPLog

    # check if the exists
    ip_query = IPLog.objects.filter(ip_address=ip_address)
    if ip_query.exists():
        # update the country
        ip_query.update(country=country)
        return

    IPLog.objects.create(ip_address=ip_address, country=country)
