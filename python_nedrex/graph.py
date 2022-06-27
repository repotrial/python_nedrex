from pathlib import Path
from typing import Any, Dict, List, Optional

from python_nedrex import config
from python_nedrex.common import check_response, download_file, http


# pylint: disable=R0913
def build_request(
    nodes: Optional[List[str]] = None,
    edges: Optional[List[str]] = None,
    ppi_evidence: Optional[List[str]] = None,
    include_ppi_self_loops: bool = False,
    taxid: Optional[List[int]] = None,
    drug_groups: Optional[List[str]] = None,
    concise: bool = True,
    include_omim: bool = True,
    disgenet_threshold: float = 0.0,
    use_omim_ids: bool = False,
    split_drug_types: bool = False,
) -> str:

    if nodes is None:
        nodes = ["disorder", "drug", "gene", "protein"]
    if edges is None:
        edges = [
            "disorder_is_subtype_of_disorder",
            "drug_has_indication",
            "drug_has_target",
            "gene_associated_with_disorder",
            "protein_encoded_by_gene",
            "protein_interacts_with_protein",
        ]
    if ppi_evidence is None:
        ppi_evidence = ["exp"]
    if taxid is None:
        taxid = [9606]
    if drug_groups is None:
        drug_groups = ["approved"]

    body = {
        "nodes": nodes,
        "edges": edges,
        "ppi_evidence": ppi_evidence,
        "ppi_self_loops": include_ppi_self_loops,
        "taxid": taxid,
        "drug_groups": drug_groups,
        "concise": concise,
        "include_omim": include_omim,
        "disgenet_threshold": disgenet_threshold,
        "use_omim_ids": use_omim_ids,
        "split_drug_types": split_drug_types,
    }

    url = f"{config.url_base}/graph/builder"
    resp = http.post(url, json=body, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result


# pylint: enable=R0913


def check_build_status(uid: str) -> Dict[str, Any]:
    url = f"{config.url_base}/graph/details/{uid}"
    resp = http.get(url, headers={"x-api-key": config.api_key})
    result: Dict[str, Any] = check_response(resp)
    return result


def download_graph(uid: str, target: Optional[str] = None) -> None:
    if target is None:
        target = str(Path(f"{uid}.graphml").resolve())

    url = f"{config.url_base}/graph/download/{uid}/{uid}.graphml"

    download_file(url, target)
