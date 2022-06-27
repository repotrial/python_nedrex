from typing import Any, Dict, List

from python_nedrex import config
from python_nedrex.common import check_response, http


def diamond_submit(
    seeds: List[str],
    n: int,  # pylint: disable=C0103
    alpha: int = 1,
    network: str = "DEFAULT",
    edges: str = "all",
) -> str:

    url = f"{config.url_base}/diamond/submit"
    body = {
        "seeds": seeds,
        "n": n,
        "alpha": alpha,
        "network": network,
        "edges": edges,
    }

    resp = http.post(url, json=body, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result


def check_diamond_status(uid: str) -> Dict[str, Any]:
    url = f"{config.url_base}/diamond/status"
    params = {"uid": uid}
    resp = http.get(url, params=params, headers={"x-api-key": config.api_key})
    result: Dict[str, Any] = check_response(resp)
    return result


def download_diamond_results(uid: str) -> str:
    url = f"{config.url_base}/diamond/download"
    params = {"uid": uid}
    resp = http.get(url, params=params, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result
