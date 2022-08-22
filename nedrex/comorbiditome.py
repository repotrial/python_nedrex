# -*- coding: utf-8 -*-
"""Functions to access the comorbiditome in NeDRex
"""

from typing import Dict as _Dict
from typing import List as _List
from typing import Literal

from nedrex import config as _config
from nedrex._common import check_response as _check_response
from nedrex._common import http as _http


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
