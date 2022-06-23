from typing import Dict, Iterable, List, Union

from python_nedrex import config
from python_nedrex.common import check_response, http


def get_encoded_proteins(gene_list: Iterable[Union[int, str]]) -> Dict[str, List[str]]:
    """
    Genes the proteins encoded by genes in a supplied gene list.

    The genes can be submitted either as a list of strings or integers.
    """
    genes = []
    for gene in gene_list:
        if isinstance(gene, int):
            gene = str(gene)
        if not isinstance(gene, str):
            raise ValueError("items in gene_list must be int or str")

        gene = gene.lower()
        if not gene.startswith("entrez."):
            genes.append(f"entrez.{gene}")
        else:
            genes.append(gene)

    url = f"{config.url_base}/relations/get_encoded_proteins"
    resp = http.get(url, params={"gene": genes}, headers={"x-api-key": config.api_key})
    result: Dict[str, List[str]] = check_response(resp)
    return result


def get_drugs_indicated_for_disorders(disorder_list: Iterable[str]) -> Dict[str, List[str]]:
    disorders = []
    for disorder in disorder_list:
        if not isinstance(disorder, str):
            raise ValueError("items in disorder_list must be str")

        if disorder.startswith("mondo."):
            disorders.append(disorder)
        else:
            disorders.append(f"mondo.{disorder}")

    url = f"{config.url_base}/relations/get_drugs_indicated_for_disorders"
    resp = http.get(url, params={"disorder": disorders}, headers={"x-api-key": config.api_key})
    result: Dict[str, List[str]] = check_response(resp)
    return result


def get_drugs_targetting_proteins(protein_list: Iterable[str]) -> Dict[str, List[str]]:
    proteins = []
    for protein in protein_list:
        if not isinstance(protein, str):
            raise ValueError("items in protein_list must be str")

        if protein.startswith("uniprot."):
            proteins.append(protein)
        else:
            proteins.append(f"uniprot.{protein}")

    url = f"{config.url_base}/relations/get_drugs_targetting_proteins"
    resp = http.get(url, params={"protein": proteins}, headers={"x-api-key": config.api_key})
    result: Dict[str, List[str]] = check_response(resp)
    return result


def get_drugs_targetting_gene_products(gene_list: Iterable[str]) -> Dict[str, List[str]]:
    genes = []
    for gene in gene_list:
        if isinstance(gene, int):
            gene = str(gene)
        if not isinstance(gene, str):
            raise ValueError("items in gene_list must be int or str")

        gene = gene.lower()
        if not gene.startswith("entrez."):
            genes.append(f"entrez.{gene}")
        else:
            genes.append(gene)

    url = f"{config.url_base}/relations/get_drugs_targetting_gene_products"
    resp = http.get(url, params={"gene": genes}, headers={"x-api-key": config.api_key})
    result: Dict[str, List[str]] = check_response(resp)
    return result
