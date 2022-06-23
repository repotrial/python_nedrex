from typing import Any, Dict, Iterable, List, Optional

from python_nedrex import config
from python_nedrex.common import (
    check_pagination_limit,
    check_response,
    get_pagination_limit,
    http,
)
from python_nedrex.exceptions import NeDRexError


def ppis(evidence: Iterable[str], skip: int = 0, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    evidence_set = set(evidence)
    extra_evidence = evidence_set - {"exp", "pred", "ortho"}
    if extra_evidence:
        raise NeDRexError(f"unexpected evidence types: {extra_evidence}")

    maximum_limit = get_pagination_limit()
    check_pagination_limit(limit, maximum_limit)

    params = {"iid_evidence": list(evidence_set), "skip": skip, "limit": limit}

    resp = http.get(f"{config.url_base}/ppi", params=params, headers={"x-api-key": config.api_key})
    result: List[Dict[str, Any]] = check_response(resp)
    return result
