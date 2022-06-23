"""Module containing functions relating to the general routes in the NeDRex API

Additionally, this module also contains routes for obtaining API keys.
"""

from typing import Any, Dict, Generator, List, Optional, cast

from python_nedrex import config
from python_nedrex.common import (
    check_pagination_limit,
    check_response,
    get_pagination_limit,
    http,
)
from python_nedrex.decorators import check_url_base
from python_nedrex.exceptions import NeDRexError


def _check_type(coll_name: str, coll_type: str) -> bool:
    if coll_type == "edge":
        if coll_name in get_edge_types():
            return True
        raise NeDRexError(f"type={coll_name!r} not in NeDRex edge types")

    if coll_type == "node":
        if coll_name in get_node_types():
            return True
        raise NeDRexError(f"type={coll_name!r} not in NeDRex node types")

    raise NeDRexError(f"_check_type received invalid coll_type={coll_type!r}")


@check_url_base
def api_keys_active() -> bool:
    """Checks whether API keys are active for the instance of NeDRex set in the config

    Returns True if the keys are active, False otherwise
    """
    url = f"{config.url_base}/api_key_setting"
    response = http.get(url)
    if response.status_code != 200:
        raise Exception("Unexpected non-200 status code")
    return cast(bool, response.json())


@check_url_base
def get_api_key(*, accept_eula: bool = False) -> Any:
    """Obtains a new API key from the NeDRex API.

    This function will only return if accept_eula is explicitly set to True
    """
    if accept_eula is not True:
        raise NeDRexError("an API key cannot be obtained unless accept_eula is set to True")

    url = f"{config.url_base}/admin/api_key/generate"
    response = http.post(url, json={"accept_eula": accept_eula})
    return response.json()


@check_url_base
def get_node_types() -> Any:
    """
    Returns the list of node types stored in NeDRexDB

        Returns:
            node_list (list[str]): List of node types in NeDRex
    """
    url: str = f"{config.url_base}/list_node_collections"
    response = http.get(url, headers={"x-api-key": config.api_key})
    node_list = check_response(response)
    return node_list


@check_url_base
def get_edge_types() -> Any:
    """
    Returns a list of edge types stored in NeDRexDB

        Returns:
            edge_list (list[str]): List of edge types in NeDRex
    """
    url: str = f"{config.url_base}/list_edge_collections"
    response = http.get(url, headers={"x-api-key": config.api_key})
    edge_list = check_response(response)
    return edge_list


@check_url_base
def get_collection_attributes(coll_type: str, include_counts: bool = False) -> Any:
    """
    Retrurns a list of the available attributes stored in NeDRex for the given type

        Parameters:
            type (str): The node or edge type to get available attributes for

        Returns:
            attr_list (list[str]): The list of available attributes for the specified node/edge type
    """
    url: str = f"{config.url_base}/{coll_type}/attributes"
    response = http.get(url, headers={"x-api-key": config.api_key}, params={"include_counts": include_counts})
    attr_list = check_response(response)
    return attr_list


@check_url_base
def get_node_ids(coll_type: str) -> Any:
    """
    Returns a list of node identifiers in NeDRex for the given type

        Parameters:
            type(str): The node type to get IDs for
        Returns:
            node_ids (list[str]): The list of available node_ids for the specified node type
    """
    _check_type(coll_type, "node")

    url: str = f"{config.url_base}/{coll_type}/attributes/primaryDomainId/json"

    resp = http.get(url, headers={"x-api-key": config.api_key})
    data = check_response(resp)
    node_ids = [i["primaryDomainId"] for i in data]
    return node_ids


@check_url_base
def get_nodes(
    node_type: str,
    attributes: Optional[List[str]] = None,
    node_ids: Optional[List[str]] = None,
    limit: Optional[int] = None,
    offset: int = 0,
) -> Any:
    """
    Returns nodes in NeDRex for the given type

        Parameters:
            node_type (str): The node type to collect
            attributes (Optional[list[str]]): A list of attributes to return for the collected nodes. The default
              (None) returns all attributes.
            node_ids (Optional[list[str]]): A list of the specific node IDs to return. The default (None) returns all
              nodes.
            limit (Optional[int]): A limit for the number of records to be returned. The maximum value for this is set
              by the API.
            offset (int): The number of records to skip before returning records. Default is 0 (no records skipped).
        Returns:
            node_ids (list[str]): The list of available node_ids for the specified node type
    """
    _check_type(node_type, "node")

    upper_limit = get_pagination_limit()
    check_pagination_limit(limit, upper_limit)

    params = {"node_id": node_ids, "attribute": attributes, "offset": offset, "limit": limit}

    resp = http.get(
        f"{config.url_base}/{node_type}/attributes/json", params=params, headers={"x-api-key": config.api_key}
    )

    items = check_response(resp)
    return items


@check_url_base
def iter_nodes(
    node_type: str, attributes: Optional[List[str]] = None, node_ids: Optional[List[str]] = None
) -> Generator[Dict[str, Any], None, None]:

    _check_type(node_type, "node")
    upper_limit = get_pagination_limit()

    params: Dict[str, Any] = {"node_id": node_ids, "attribute": attributes, "limit": upper_limit}

    offset = 0
    while True:
        params["offset"] = offset
        resp = http.get(
            f"{config.url_base}/{node_type}/attributes/json", params=params, headers={"x-api-key": config.api_key}
        )

        data = check_response(resp)

        for doc in data:
            yield doc

        if len(data) < upper_limit:
            break
        offset += upper_limit


@check_url_base
def get_edges(edge_type: str, limit: Optional[int] = None, offset: Optional[int] = None) -> Any:
    """
    Returns edges in NeDRex of the given type

        Parameters:
            edge_type (str): The node type to collect
            limit (Optional[int]): A limit for the number of records to be returned. The maximum value for this is set
              by the API.
            offset (int): The number of records to skip before returning records. Default is 0 (no records skipped).
    """
    _check_type(edge_type, "edge")

    params = {"limit": limit, "offset": offset, "api_key": config.api_key}

    resp = http.get(f"{config.url_base}/{edge_type}/all", params=params, headers={"x-api-key": config.api_key})
    items = check_response(resp)
    return items


@check_url_base
def iter_edges(edge_type: str) -> Generator[Dict[str, Any], None, None]:
    _check_type(edge_type, "edge")
    upper_limit = get_pagination_limit()

    offset = 0
    while True:
        params = {"offset": offset, "limit": upper_limit}
        resp = http.get(f"{config.url_base}/{edge_type}/all", params=params, headers={"x-api-key": config.api_key})
        data = check_response(resp)

        for doc in data:
            yield doc

        if len(data) < upper_limit:
            break
        offset += upper_limit
