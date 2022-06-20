from typing import Any

import requests  # type: ignore

from python_nedrex import config


def get_pagination_limit() -> Any:
    url = f"{config.url_base}/pagination_max"
    return requests.get(url, headers={"x-api-key": config.api_key}).json()
