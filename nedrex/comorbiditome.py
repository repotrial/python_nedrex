# -*- coding: utf-8 -*-
"""Functions to access the comorbiditome in NeDRex
"""

from pathlib import Path
from typing import Dict as _Dict
from typing import List as _List
from typing import Literal
from typing import Optional as _Optional
from typing import Union as _Union
from urllib.request import urlretrieve

from nedrex import config as _config
from nedrex._common import check_response as _check_response
from nedrex._common import check_status_factory as _check_status_factory
from nedrex._common import http as _http

__all__ = [
    "map_icd10_to_mondo",
    "map_mondo_to_icd10",
    "get_icd10_associations",
    "submit_comorbiditome_build",
]


def map_icd10_to_mondo(disorders: _List[str]) -> _Dict[str, _List[str]]:
    url = f"{_config.url_base}/comorbiditome/icd10_to_mondo"

    params = {"icd10": disorders}
    headers = {"x-api-key": _config.api_key}

    response = _http.get(url, params=params, headers=headers)
    result: _Dict[str, _List[str]] = _check_response(response)
    return result


def map_mondo_to_icd10(
    disorders: _List[str], only_3char: bool = False, exclude_3char: bool = False
) -> _Dict[str, _List[str]]:
    url = f"{_config.url_base}/comorbiditome/mondo_to_icd10"

    params = {"mondo": disorders, "only_3char": only_3char, "exclude_3char": exclude_3char}
    headers = {"x-api-key": _config.api_key}

    response = _http.get(url, params=params, headers=headers)
    result: _Dict[str, _List[str]] = _check_response(response)
    return result


_EdgeTypes = Literal[
    "gene_associated_with_disorder",
    "drug_has_indication",
    "drug_has_contraindication",
    "drug_targets_disorder_associated_gene_product",
]


def get_icd10_associations(nodes: _List[str], edge_type: _EdgeTypes) -> _Dict[str, _List[str]]:
    url = f"{_config.url_base}/comorbiditome/get_icd10_associations"

    params = {"node": nodes, "edge_type": edge_type}
    headers = {"x-api-key": _config.api_key}

    response = _http.get(url, params=params, headers=headers)
    result: _Dict[str, _List[str]] = _check_response(response)
    return result


def submit_comorbiditome_build(
    max_phi_cor: _Optional[float] = None,
    min_phi_cor: _Optional[float] = None,
    max_p_value: _Optional[float] = None,
    min_p_value: _Optional[float] = None,
    mondo: _Optional[list[str]] = None,
) -> str:
    url = f"{_config.url_base}/comorbiditome/submit_comorbiditome_build"

    body = {
        "mondo": mondo,
        "max_phi_cor": max_phi_cor,
        "min_phi_cor": min_phi_cor,
        "max_p_value": max_p_value,
        "min_p_value": min_p_value,
    }
    headers = {"x-api-key": _config.api_key}

    response = _http.post(url, json=body, headers=headers)
    result: str = _check_response(response)
    return result


check_comorbiditome_status = _check_status_factory("/comorbiditome/comorbiditome_build_status")
check_comorbiditome_status.__name__ = "check_comorbiditome_status"
check_comorbiditome_status.__doc__ = """Gets details of a submitted comorbiditome build job

    Parameters
    ----------
    uid : str
        The unique ID of a comorbiditome build job

    Returns
    -------
    dict[str, Any]
        Details of the current comorbiditome build job; the status of job
        is stored using the `status` key
"""


_Formats = Literal["tsv", "graphml"]


def download_comorbiditome_build(uid: str, fmt: _Formats, save_path: _Optional[str] = None) -> _Union[str, None]:
    if save_path is None:
        filename = "none.txt"
    else:
        filename = Path(save_path).name

    url = f"{_config.url_base}/comorbiditome/download_comorbiditome_build/" f"{uid}/{fmt}/{filename}"

    if save_path:
        urlretrieve(url, save_path)  # nosec
        return None

    response = _http.get(url)
    result: str = _check_response(response, return_type="text")
    return result
