# -*- coding: utf-8 -*-
"""Functions to run the DIAMOnD routes in a NeDRex API instance

As described in Sadegh et al, 2021, DIAMOnD identifies a candidate disease
module around a set of known disease genes (seeds) by greedily adding
nodes with a high connectivity significance to the modules.
"""
from typing import List as _List

from nedrex import config as _config
from nedrex.common import check_response as _check_response
from nedrex.common import check_status_factory as _check_status_factory
from nedrex.common import http as _http

__all__ = ["diamond_submit", "check_diamond_status", "download_diamond_results"]


def diamond_submit(
    seeds: _List[str],
    n: int,  # pylint: disable=C0103
    alpha: int = 1,
    network: str = "DEFAULT",
    edges: str = "all",
) -> str:
    """Submit a request to NeDRex to run DIAMOnD analysis

    Parameters
    ----------
    seeds : list[str]
        A list of seed genes or proteins with which to run DIAMOnD
    n : int
        The maximum number of nodes at which to stop the algorithm
    alpha : int, optional
        Weight given to seeds. The default value is 1.
    network : str, optional
        NeDRexDB-based network to run DIAMOnD analysis with. The default
        network, `DEFAULT` uses a GGI/PPI network based on experimental
        PPIs.
    edges : str, optional
        Option affecting which edges are returned in the results. Options
        are `all`, which return edges in the GGI/PPI between nodes in the
        DIAMOnD module, and `limited`, which only return edges between
        seeds and new nodes. The default is `all`.

    Returns
    -------
    uid : str
        The unique ID of the DIAMOnD job.
    """
    if edges not in {"limited", "all"}:
        raise ValueError(f"invalid value for argument edges ({edges!r}), should be all|limited")

    url = f"{_config.url_base}/diamond/submit"
    body = {
        "seeds": seeds,
        "n": n,
        "alpha": alpha,
        "network": network,
        "edges": edges,
    }

    resp = _http.post(url, json=body, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp)
    return result


check_diamond_status = _check_status_factory("/diamond/status")
check_diamond_status.__name__ = "check_diamond_status"
check_diamond_status.__doc__ = """Returns details of a submitted DIAMOnD job

    Parameters
    ----------
    uid : str
        The unique ID of a DIAMOnD job

    Returns
    -------
    result : dict[str, Any]
        Details of the DIAMOnD job with the given unique ID; the status of
        the job is stored using the `status` key
"""


def download_diamond_results(uid: str) -> str:
    """Downloads the results of a completed DIAMOnD job

    Parameters
    ----------
    uid : str
        The unique ID of a DIAMOnD job

    Returns
    -------
    result : str
        A string containing the DIAMOnD results
    """
    url = f"{_config.url_base}/diamond/download"
    params = {"uid": uid}
    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp, return_type="text")
    return result
