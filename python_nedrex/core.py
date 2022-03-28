from multiprocessing.sharedctypes import Value
from typing import Any, Optional
import requests

from python_nedrex import config
from python_nedrex.decorators import check_url_base
from python_nedrex.exceptions import NeDRexError


@check_url_base
def get_node_types() -> list[str]:
    """
    Returns the list of node types stored in NeDRexDB

        Returns:
            node_list (list[str]): List of node types in NeDRex
    """
    url: str = f"{config._url_base}/list_node_collections"
    node_list = requests.get(url).json()
    return node_list


@check_url_base
def get_edge_types() -> list[str]:
    """
    Returns a list of edge types stored in NeDRexDB

        Returns:
            edge_list (list[str]): List of edge types in NeDRex
    """
    url: str = f"{config._url_base}/list_edge_collections"
    edge_list = requests.get(url).json()
    return edge_list


@check_url_base
def get_collection_attributes(type: str) -> list[str]:
    """
    Retrurns a list of the available attributes stored in NeDRex for the given type

        Parameters:
            type (str): The node or edge type to get available attributes for

        Returns:
            attr_list (list[str]): The list of available attributes for the specified node/edge type
    """
    url: str = f"{config._url_base}/{type}/attributes"
    attr_list = requests.get(url).json()
    return attr_list


@check_url_base
def get_node_ids(type: str):
    """
    Returns a list of node identifiers in NeDRex for the given type

        Parameters:
            type(str): The node type to get available attributes for
        Returns:
            node_ids (list[str]): The list of available node_ids for the specified node type
    """
    if type not in get_node_types():
        raise NeDRexError(f"{type=} not in NeDRex node types")
    url: str = f"{config._url_base}/{type}/attributes/primaryDomainId/json"
    node_ids = [i["primaryDomainId"] for i in requests.get(url).json()]
    return node_ids


@check_url_base
def get_nodes(
    type: str, attributes: Optional[list[str]] = None, node_ids: Optional[list[str]] = None
) -> list[dict[str, Any]]:

    if type not in get_node_types():
        raise NeDRexError(f"{type=} not in NeDRex node types")

    if attributes is None:
        attributes = get_collection_attributes(type)

    if node_ids is None:
        node_ids = get_node_ids(type)

    body = {"node_ids": node_ids, "attributes": attributes}

    items = requests.get(f"{config._url_base}/{type}/attributes_v2/json", json=body).json()
    return items


@check_url_base
def get_edges(
    type: str,
):
    if type not in get_edge_types():
        raise ValueError(f"{type=} not in edge types")
    
    items = requests.get(f"{config._url_base}/{type}/all").json()

    return items
