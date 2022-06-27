from typing import List, Optional

from python_nedrex import config
from python_nedrex.common import check_response, http


def trustrank_submit(
    seeds: List[str],
    damping_factor: float = 0.85,
    only_direct_drugs: bool = True,
    only_approved_drugs: bool = True,
    n: Optional[int] = None,  # pylint: disable=C0103
) -> str:
    url = f"{config.url_base}/trustrank/submit"

    body = {
        "seeds": seeds,
        "damping_factor": damping_factor,
        "only_direct_drugs": only_direct_drugs,
        "only_approved_drugs": only_approved_drugs,
        "N": n,
    }

    resp = http.post(url, json=body, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result
