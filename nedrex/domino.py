# -*- coding: utf-8 -*-
"""Functions to run DOMINO routes in a NeDRex API instance

As described by Levi et al. (2021), DOMINO is an algorithm for detecting
active network modules.
"""
from typing import List as _List

from nedrex import config as _config
from nedrex.common import check_response as _check_response
from nedrex.common import check_status_factory as _check_status_factory
from nedrex.common import http as _http


def domino_submit(seeds: _List[str], network: str = "DEFAULT") -> str:
    """Submit a request to NeDRex to run DOMINO analysis

    Parameters
    ----------
    seeds : list[str]
        A list of seed genes or proteins with which to run DOMINO analysis
    network : str, optional
        NeDRexDB-based network to run DOMINO analysis with. The defaut
        network, `DEFAULT` uses a GGI/PPI network based on experimental
        PPIs.

    Returns
    -------
    uid : str
        The unique ID of the DOMINO job.
    """
    url = f"{_config.url_base}/domino/submit"
    body = {"seeds": seeds, "network": network}

    resp = _http.post(url, json=body, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp)
    return result


check_domino_status = _check_status_factory("/domino/status")
check_domino_status.__name__ = "check_domino_status"
check_domino_status.__doc__ = """Returns details of a submitted DOMINO job

    Parameters
    ----------
    uid : str
        The unique ID of a DOMINO job

    Returns
    -------
    result : dict[str, Any]
        Details of the DOMINO job with the given unique ID; the status of
        the job is stored using the `status` key
"""
