# -*- coding: utf-8 -*-
"""Functions to run TrustRank analysis routes in a NeDRex API instance

As described in Sadegh et al, 2021, "TrustRank is a modification of Google's
PageRank algorithm, where the initial trust score is iteratively propagated
from seed nodes to adjest nodes using the network topology. It prioritises
nodes in a network based on how well they are connected to a (trusted) set of
seed nodes."
"""

from typing import List as _List
from typing import Optional as _Optional

from nedrex import config as _config
from nedrex._common import check_response as _check_response
from nedrex._common import check_status_factory as _check_status_factory
from nedrex._common import http as _http

__all__ = ["trustrank_submit", "check_trustrank_status", "download_trustrank_results"]


def trustrank_submit(
    seeds: _List[str],
    damping_factor: float = 0.85,
    only_direct_drugs: bool = True,
    only_approved_drugs: bool = True,
    n: _Optional[int] = None,  # pylint: disable=C0103
) -> str:
    """Submit a job to the NeDRexAPI to run TrustRank analysis

    Parameters
    ----------
    seeds : list[str]
        A list of seed proteins with which to run TrustRank analysis
    damping_factor : float, optional
        The damping factor value, which controls rate of trust propagation
        across the network. The default is 0.85
    only_direct_drugs : bool, optional
        Specifies whether to return only drugs that target the seed nodes.
        The default, True, only returns drugs that target seed nodes
    only_approved_drugs : bool, optional
        Specifies whether to filter drugs that are not approved. The default,
        filters non-approved drugs (True)
    n : int, optional
        The number of results to return. If there are additional results that
        have the same score as the n-th highest ranking drug, these are also
        returned

    Returns
    -------
    str
        The UID for the TrustRank job
    """
    url = f"{_config.url_base}/trustrank/submit"

    body = {
        "seeds": seeds,
        "damping_factor": damping_factor,
        "only_direct_drugs": only_direct_drugs,
        "only_approved_drugs": only_approved_drugs,
        "N": n,
    }

    resp = _http.post(url, json=body, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp)
    return result


check_trustrank_status = _check_status_factory("/trustrank/status")
check_trustrank_status.__name__ = "check_trustrank_status"
check_trustrank_status.__doc__ = """Gets details of a submitted TrustRank analysis job

    Parameters
    ----------
    uid : str
        The unique ID of a TrustRank job

    Returns
    -------
    dict[str, Any]
        Details of the TrustRank job; the status of job is stored using the
        `status` key
"""


def download_trustrank_results(uid: str) -> str:
    """Downloads results of a TrustRank analysis job

    Parameters
    ----------
    uid : str
        The unique ID of a TrustRank job

    Returns
    -------
    str
        A string containing the TrustRank analysis results
    """
    url = f"{_config.url_base}/trustrank/download"
    params = {"uid": uid}

    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp, return_type="text")
    return result
