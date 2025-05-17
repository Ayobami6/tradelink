import os
from typing import Any, List, Union, Tuple, Dict
from dotenv import load_dotenv
from django.db.models.query import QuerySet
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
import string
import random
import requests


load_dotenv()


def get_env(key: str, fallback: str) -> str:
    """get environment variable value from .env

    Args:
        key (str): variable key
        fallback (str): fallback value if none

    Returns:
        str: value of environment variable
    """
    return os.getenv(key, fallback)


def paginate(
    data: Union[List[Any], QuerySet],
    page: int,
    request: Any,
    page_size: int = 10,
    serializer: Any = None,
    data_key: str = "results",
) -> Union[Dict[str, Any], Tuple]:  # Fixed union syntax
    """Paginate the data and return the paginated data"""
    paginator = Paginator(data, page_size)
    request_url = request.build_absolute_uri()
    print("Lets see the request url :", request_url)
    next_url = f"{request_url}?page={int(page) + 1}"
    prev_number = int(page) - 1
    prev_url = f"{request_url}?page={prev_number}" if prev_number > 0 else None

    try:
        data_page = paginator.page(page)
    except PageNotAnInteger:
        data_page = paginator.page(1)
    except EmptyPage:
        data_page = paginator.page(paginator.num_pages)

    total_pages = paginator.num_pages
    current_page = data_page.number
    count = paginator.count
    # if data is an instance of a queryset, serialize
    if isinstance(data, QuerySet):
        if not serializer:
            raise Exception("Serializer must be provided for QuerySet")
        jsonified_data = serializer(data_page, many=True).data
    else:
        jsonified_data = data_page

    resp = {
        "count": count,
        "total_pages": total_pages,
        "current_page": current_page,
        "next": next_url,
        "previous": prev_url,
        data_key: jsonified_data,
    }
    return resp


def generate_ref() -> str:
    """Generates unique string"""
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return code.upper()


class PaystackSDK:
    """Paystack SDK"""

    def __init__(self) -> None:
        self.secret_key = get_env("PAYSTACK_SECRET_KEY", "")
        self.base_url = "https://api.paystack.co/transaction/initialize"
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    # initialize transaction
    def initialize_transaction(self, data: dict, main_amount: int) -> Union[bool, dict]:
        """Initialize transaction"""
        from app.models import AppSetting
        from orders.models import PaystackTransaction

        # get the app settings for whatsapp redirect
        app_setting = AppSetting.objects.all()[0]
        data["callback_url"] = app_setting.whatapp_business_url
        response = requests.post(self.base_url, headers=self.headers, json=data)
        if response.status_code == 200:
            # save the transaction
            PaystackTransaction.create_record(
                order_ref=data["reference"],
                amount=int(main_amount),
                customer_email=data["email"],
                gateway_response=response.json(),
            )
            return True, response.json()
        else:
            print("API Response: ", response.text)
            return False, {}


def get_country_currency_from_ip(ip_addr: str) -> str:
    """Get country from IP address"""
    token = get_env("IPINFO_TOKEN", "")
    response = requests.get(f"https://ipinfo.io/{ip_addr}/json?token={token}")
    if response.status_code == 200:
        print("This is the currenct: ", response.json())
        return response.json()
    else:
        print("API Response: ", response.text)
        return ""
