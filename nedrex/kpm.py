from typing import List as _List

from nedrex import config as _config
from nedrex.common import check_response as _check_response
from nedrex.common import check_status_factory as _check_status_factory
from nedrex.common import http as _http


def kpm_submit(seeds: _List[str], k: int, network: str = "DEFAULT") -> str:
    """Submit a request to a NeDRex instance to run KPM analysis

    Parameters
    ----------
    seeds : list[str]
        A list of seed genes or proteins with which to run KPM analysis
    k : int
        The number of gene or protein exceptions to allow in KPM analysis
    network : str, optional
        NeDRexDB-based network to run DOMINO analysis with. The defaut
        network, `DEFAULT` uses a GGI/PPI network based on experimental
        PPIs.

    Returns
    -------
    uid : str
        The unique ID of a KPM job.
    """
    url = f"{_config.url_base}/kpm/submit"
    body = {"seeds": seeds, "k": k, "network": network}

    resp = _http.post(url, json=body, headers={"x-api-key": _config.api_key})
    result: str = _check_response(resp)
    return result


check_kpm_status = _check_status_factory("/kpm/status")
check_kpm_status.__name__ = "check_kpm_status"
check_kpm_status.__doc__ = """Returns details of a submitted KPM job

    Parameters
    ----------
    uid : str
        The unique ID of a KPM job

    Returns
    -------
    result : dict[str, Any]
        Details of the KPM job with the given unique ID; the status of the
        job is stored using the `status` key
"""
