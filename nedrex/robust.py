# -*- coding: utf-8 -*-
"""Functions to access the ROBUST routes in a NeDRex API instance

As described in Bernett, et al. (2022), ROBUST carries out robust disease
module mining via enumeration of diverse prise-collecting Steiner trees.
"""

from typing import List as _List

from nedrex import config as _config
from nedrex._common import check_response as _check_response
from nedrex._common import check_status_factory as _check_status_factory
from nedrex._common import http as _http

__all__ = ["robust_submit", "check_robust_status", "download_robust_results"]


# pylint: disable=R0913
def robust_submit(
    seeds: _List[str],
    network: str = "DEFAULT",
    initial_fraction: float = 0.25,
    reduction_factor: float = 0.9,
    num_trees: int = 30,
    threshold: float = 0.1,
) -> str:
    """Submits a request to run ROBUST analysis

    Parameters
    ----------
    seeds : list[str]
        A list of seed proteins with which to run ROBUST analysis
    network : str, optional
        NeDRexDB-based network to run ROBUST analysis with. The default
        network, DEFAULT uses a GGI/PPI network based on experimental PPIs
    initial_fraction : float, optional
        The initial fraction to use for ROBUST, by default 0.25
    reduction_factor : float, optional
        The reduction factor to use for ROBUST, by default 0.9
    num_trees : int, optional
        The number of Steiner trees to be computed, by default 30
    threshold : float, optional
        The threshold value to use for ROBUST, by default 0.1

    Returns
    -------
    str
        The UID of the ROBUST analysis job.
    """

    body = {
        "seeds": seeds,
        "network": network,
        "initial_fraction": initial_fraction,
        "reduction_factor": reduction_factor,
        "num_trees": num_trees,
        "threshold": threshold,
    }
    url = f"{_config.url_base}/robust/submit"

    resp = _http.post(url, json=body, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp)
    return result


# pylint: enable=R0913

check_robust_status = _check_status_factory("/robust/status")
check_robust_status.__name__ = "check_robust_status"
check_robust_status.__doc__ = """Gets details of a submitted ROBUST job

    Parameters
    ----------
    uid : str
        The unique ID of a ROBUST job

    Returns
    -------
    dict[str, Any]
        Details of the ROBUST job; the status of job is stored using the
        `status` key
"""


def download_robust_results(uid: str) -> str:
    """Downloads results of a ROBUST analysis job

    Parameters
    ----------
    uid : str
        The unique ID of a ROBUST job

    Returns
    -------
    str
        A string containing the ROBUST analysis results
    """
    url = f"{_config.url_base}/robust/results"
    params = {"uid": uid}

    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp, return_type="text")
    return result
