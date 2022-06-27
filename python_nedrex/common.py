import urllib.request
from typing import Any, Optional

import requests  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from urllib3.util.retry import Retry  # type: ignore

from python_nedrex import config
from python_nedrex.exceptions import ConfigError, NeDRexError

# Start - code derived from https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
DEFAULT_TIMEOUT = 120


class TimeoutHTTPAdapter(HTTPAdapter):  # type: ignore
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    # pylint: disable=arguments-differ
    def send(self, request: requests.Request, **kwargs: Any) -> requests.Response:
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

http = requests.Session()
adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)
http.mount("https://", adapter)
http.mount("http://", adapter)
# End - code derived from https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/


def check_response(resp: requests.Response) -> Any:
    data = resp.json()

    if resp.status_code == 401:
        if data["detail"] == "An API key is required to access the requested data":
            raise ConfigError("no API key set in the configuration")

    if resp.status_code == 422:
        raise NeDRexError(data["detail"])

    if resp.status_code == 404:
        raise NeDRexError("not found")

    return data


def get_pagination_limit() -> Any:
    url = f"{config.url_base}/pagination_max"
    return requests.get(url, headers={"x-api-key": config.api_key}).json()


def check_pagination_limit(limit: Optional[int], upper_limit: int) -> None:
    if limit and upper_limit < limit:
        raise NeDRexError(f"limit={limit:,} is too great (maximum is {upper_limit:,})")


def download_file(url: str, target: str) -> None:
    if config.api_key is not None:
        opener = urllib.request.build_opener()
        opener.addheaders = [("x-api-key", config.api_key)]
        urllib.request.install_opener(opener)

    try:
        urllib.request.urlretrieve(url, target)
    except urllib.error.HTTPError as err:
        if err.code == 404:
            raise NeDRexError("not found") from err
        raise NeDRexError("unexpected failure") from err
