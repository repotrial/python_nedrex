from typing import Any, Dict, Optional

from python_nedrex import config
from python_nedrex.common import check_response, download_file, http


def get_metadata() -> Dict[str, Any]:
    url = f"{config.url_base}/static/metadata"
    resp = http.get(url, headers={"x-api-key": config.api_key})
    result: Dict[str, Any] = check_response(resp)
    return result


def get_license() -> str:
    url = f"{config.url_base}/static/license"
    resp = http.get(url)
    result: str = check_response(resp)
    return result


def download_lengths_map(target: Optional[str] = None) -> None:
    if target is None:
        target = "lengths.map"

    url = f"{config.url_base}/static/lengths.map"

    download_file(url, target)
