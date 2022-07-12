# -*- coding: utf-8 -*-
"""Functions to run closeness centrality routes in a NeDRex API instance

As described in Sadegh et al, 2021, closeness centrality (CC) is a node
centrality measure that prioritizes nodes in a network based on the
lengths of their shortest paths to all other nodes in a network. NeDRex
implements a modified version where closeness is calulcated with respect
to selected seeds.
"""

from typing import List as _List
from typing import Optional as _Optional

from nedrex import config as _config
from nedrex.common import check_response as _check_response
from nedrex.common import check_status_factory as _check_status_factory
from nedrex.common import http as _http

__all__ = [
    "closeness_submit",
    "check_closeness_status",
    "download_closeness_results",
]


def closeness_submit(
    seeds: _List[str],
    only_direct_drugs: bool = True,
    only_approved_drugs: bool = True,
    N: _Optional[int] = None,  # pylint: disable=C0103
) -> str:
    """Submit a request to NeDRex to run closeness centrality analysis

    Parameters
    ----------
    seeds : list[str]
        A list of seed proteins with which to run closeness centrality
        analysis
    only_direct_drugs: bool, optional
        True (default) returns only drugs that target seeds; False
        also includes drugs in the vicinity of seeds
    only_approved_drugs: bool, optional
        True (default) returns only drugs that have an approved use, False
        will also return drugs that are not approved (e.g., experimental)
    N: int, optional
        The number of drugs to return. If, when ordered by rank, there are
        additional drugs with the same score of the Nth drug, then these
        drugs are also returned.

    Returns
    -------
    uid: str
        The unique ID of the closness centrality job.
    """
    url = f"{_config.url_base}/closeness/submit"

    body = {"seeds": seeds, "only_direct_drugs": only_direct_drugs, "only_approved_drugs": only_approved_drugs, "N": N}

    resp = _http.post(url, json=body, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp)
    return result


check_closeness_status = _check_status_factory("/closeness/status")
check_closeness_status.__name__ = "check_closeness_status"
check_closeness_status.__doc__ = """Gets details of a submitted closeness centrality job

    Parameters
    ----------
    uid : str
        The unique ID of a BiCoN job

    Returns
    -------
    result : dict[str, Any]
        Details of the current closeness centrality job; the status of job
        is stored using the `status` key
"""


def download_closeness_results(uid: str) -> str:
    """Downloads results of a completed closeness centrality job

    Parameters
    ----------
    uid : str
        The unique ID of a BiCoN job

    Returns
    -------
    result : str
        A string containing the closeness centrality results
    """
    url = f"{_config.url_base}/closeness/download"
    params = {"uid": uid}
    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp, return_type="text")
    return result
