from typing import Any, Dict, List

from python_nedrex import config
from python_nedrex.common import check_response, http


def kpm_submit(seeds: List[str], k: int, network: str = "DEFAULT") -> str:

    url = f"{config.url_base}/kpm/submit"
    body = {"seeds": seeds, "k": k, "network": network}

    resp = http.post(url, json=body, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result


def check_kpm_status(uid: str) -> Dict[str, Any]:

    url = f"{config.url_base}/kpm/status"
    params = {"uid": uid}

    resp = http.get(url, params=params, headers={"x-api-key": config.api_key})
    result: Dict[str, Any] = check_response(resp)
    return result
