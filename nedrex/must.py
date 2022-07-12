# -*- coding: utf-8 -*-
"""Functions to run MuST routes in a NeDRex API instance

As described in Sadegh et al., 2021, MuSt extracts a connected subnetwork
which potentially incorporates the genes/proteins involved in a disease
pathway/mechanism.
"""
from typing import List as _List

from nedrex import config as _config
from nedrex.common import check_response as _check_response
from nedrex.common import check_status_factory as _check_status_factory
from nedrex.common import http as _http


# pylint: disable=R0913
def must_request(
    seeds: _List[str],
    hubpenalty: float,
    multiple: bool,
    trees: int,
    maxit: int,
    network: str = "DEFAULT",
) -> str:
    """Submit a request to a NeDRex instance to run MuST analysis

    Parameters
    ----------
    seeds : list[str]
        A list of seed genes or proteins with which to run MuST analysis
    hubpenalty : float
        The penalty for hub nodes in the MuST algorithm. Setting a
        non-zero hubpenalty extracts mechanisms more specific to the
        disorder of interest.
    multiple : bool
        A parameter indicating whether or not to return multiple resulting
        Steiner trees from MuST.
    maxit : int
        The maximum number of iterations to run MuST for.
    network : str, optional
        NeDRexDB-based network to run MuST analysis with. The default
        network, `DEFAULT` uses a GGI/PPI network based on experimental
        PPIs.

    Returns
    -------
    uid : str
        The Unique ID of the MuST job

    """
    body = {
        "seeds": seeds,
        "network": network,
        "hubpenalty": hubpenalty,
        "multiple": multiple,
        "trees": trees,
        "maxit": maxit,
    }

    url = f"{_config.url_base}/must/submit"
    resp = _http.post(url, json=body, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp)
    return result


# pylint: enable=R0913


check_must_status = _check_status_factory("/must/status")
check_must_status.__name__ = "check_must_status"
check_must_status.__doc__ = """Returns details of a submitted MuST job

    Parameters
    ----------
    uid : str
        The unique ID of a MuST job

    Returns
    -------
    result : dict[str, Any]
        Details of the MuST job with the given unique ID; the status of
        the job is stored using the `status` key

"""
