from typing import Any, Dict, List

from python_nedrex import config
from python_nedrex.common import check_response, http


# pylint: disable=R0913
def robust_submit(
    seeds: List[str],
    network: str = "DEFAULT",
    initial_fraction: float = 0.25,
    reduction_factor: float = 0.9,
    num_trees: int = 30,
    threshold: float = 0.1,
) -> str:

    body = {
        "seeds": seeds,
        "network": network,
        "initial_fraction": initial_fraction,
        "reduction_factor": reduction_factor,
        "num_trees": num_trees,
        "threshold": threshold,
    }
    url = f"{config.url_base}/robust/submit"

    resp = http.post(url, json=body, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result


# pylint: enable=R0913


def check_robust_status(uid: str) -> Dict[str, Any]:
    url = f"{config.url_base}/robust/status"
    params = {"uid": uid}

    resp = http.get(url, params=params, headers={"x-api-key": config.api_key})
    result: Dict[str, Any] = check_response(resp)
    return result


def download_robust_results(uid: str) -> str:
    url = f"{config.url_base}/robust/results"
    params = {"uid": uid}

    resp = http.get(url, params=params, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result
