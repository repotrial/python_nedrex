from typing import Any, Dict, List

from python_nedrex import config
from python_nedrex.common import check_response, http


# pylint: disable=R0913
def must_request(
    seeds: List[str],
    hubpenalty: float,
    multiple: bool,
    trees: int,
    maxit: int,
    network: str = "DEFAULT",
) -> str:
    body = {
        "seeds": seeds,
        "network": network,
        "hubpenalty": hubpenalty,
        "multiple": multiple,
        "trees": trees,
        "maxit": maxit,
    }

    url = f"{config.url_base}/must/submit"
    resp = http.post(url, json=body, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result


# pylint: enable=R0913


def check_must_status(uid: str) -> Dict[str, Any]:
    url = f"{config.url_base}/must/status"
    resp = http.get(url, params={"uid": uid})
    result: Dict[str, Any] = check_response(resp)
    return result
