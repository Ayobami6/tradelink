import os
from typing import Any, List, Union, Tuple, Dict
from dotenv import load_dotenv
from django.db.models.query import QuerySet
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

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
    base_url = request_url.rsplit("/", 2)[0] + "/"
    next_url = f"{base_url}?page={int(page) + 1}/"
    prev_number = int(page) - 1
    prev_url = f"{base_url}?page={prev_number}" if prev_number > 0 else None

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
