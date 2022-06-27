from typing import Any, Dict, List

from python_nedrex import config
from python_nedrex.common import check_response, http


def domino_submit(seeds: List[str], network: str = "DEFAULT") -> str:
    url = f"{config.url_base}/domino/submit"
    body = {"seeds": seeds, "network": network}

    resp = http.post(url, json=body, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result


def check_domino_status(uid: str) -> Dict[str, Any]:
    url = f"{config.url_base}/domino/status"

    resp = http.get(url, params={"uid": uid}, headers={"x-api-key": config.api_key})
    result: Dict[str, Any] = check_response(resp)
    return result
