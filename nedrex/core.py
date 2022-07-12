"""Module containing functions relating to the general routes in the NeDRex API

This module contains functions that access the general routes, and also routes
for obtaining API keys.
"""

from typing import Any as _Any
from typing import Dict as _Dict
from typing import Generator as _Generator
from typing import List as _List
from typing import Optional as _Optional
from typing import cast as _cast

from nedrex import config as _config
from nedrex.common import check_pagination_limit as _check_pagination_limit
from nedrex.common import check_response as _check_response
from nedrex.common import get_pagination_limit as _get_pagination_limit
from nedrex.common import http as _http
from nedrex.decorators import check_url_base as _check_url_base
from nedrex.exceptions import NeDRexError as _NeDRexError


def _check_type(coll_name: str, coll_type: str) -> bool:
    if coll_type == "edge":
        if coll_name in get_edge_types():
            return True
        raise _NeDRexError(f"type={coll_name!r} not in NeDRex edge types")

    if coll_type == "node":
        if coll_name in get_node_types():
            return True
        raise _NeDRexError(f"type={coll_name!r} not in NeDRex node types")

    raise _NeDRexError(f"_check_type received invalid coll_type={coll_type!r}")


@_check_url_base
def api_keys_active() -> bool:
    """Checks whether API keys are active for the instance of NeDRex set in the config

    Returns
    -------
        active: bool
            True if the API keys are required, otherwise False.
    """
    url = f"{_config.url_base}/api_key_setting"
    response = _http.get(url)
    if response.status_code != 200:
        raise Exception("Unexpected non-200 status code")
    active = _cast(bool, response.json())
    return active


@_check_url_base
def get_api_key(*, accept_eula: bool = False) -> str:
    """Obtains a new API key for the NeDRex API.

    Parameters
    ----------
        accept_eula : bool
            Parameter reflecting whether the user of the library accepts
            the terms of the NeDRex end user licence agreement (EULA).
            Defaults to False. Must be set to True to acquire an API key.

    Returns
    -------
        api_key: str
            An API key that can be used to access the NeDRex platform.
    """
    if accept_eula is not True:
        raise _NeDRexError("an API key cannot be obtained unless accept_eula is set to True")

    url = f"{_config.url_base}/admin/api_key/generate"
    response = _http.post(url, json={"accept_eula": accept_eula})
    api_key = _cast(str, _check_response(response))
    return api_key


@_check_url_base
def get_node_types() -> _List[str]:
    """Gets a list of the node types stored in NeDRexDB

    Returns
    -------
    node_list: list[str]
        A list of node types in NeDRexDB
    """
    url: str = f"{_config.url_base}/list_node_collections"
    response = _http.get(url, headers={"x-api-key": _config.api_key})
    node_list = _cast(_List[str], _check_response(response))
    return node_list


@_check_url_base
def get_edge_types() -> _List[str]:
    """Gets a list of the edge types stored in NeDRexDB

    Returns
    -------
    edge_list: list[str]
        A list of edge types in NeDRexDB
    """
    url: str = f"{_config.url_base}/list_edge_collections"
    response = _http.get(url, headers={"x-api-key": _config.api_key})
    edge_list = _cast(_List[str], _check_response(response))
    return edge_list


@_check_url_base
def get_collection_attributes(coll_type: str, include_counts: bool = False) -> _Any:
    """Gets the available attributes in NeDRex for the given type

    Parameters
    ----------
    coll_type: str
        The name of the collection
    include_counts: bool, optional
        If True, returns the counts for each attribute. If False, just
        returns a list of the attributes. Default is False.

    Returns
    -------
    attributes: Union[Dict[str, Any], List[str]]
        If include_counts is False, this returns a list of the attributes
        that members of the collections have. If include_counts is true,
        this returns a dictionary that includes the counts.

    Examples
    --------
    >>> get_collection_attributes(protein)
    ['primaryDomainId',
     'comments',
     'created',
     'dataSources',
     'displayName',
     'domainIds',
     'geneName',
     'sequence',
     'synonyms',
     'taxid',
     'type',
     'updated']

    >>> get_collection_attributes(protein, include_counts=True)
    {'attribute_counts': {'comments': 204906,
                          'created': 204906,
                          'dataSources': 204906,
                          'displayName': 204906,
                          'domainIds': 204906,
                          'geneName': 204906,
                          'primaryDomainId': 204906,
                          'sequence': 204906,
                          'synonyms': 204906,
                          'taxid': 204906,
                          'type': 204906,
                          'updated': 204906},
     'document_count': 204906}
    """
    url: str = f"{_config.url_base}/{coll_type}/attributes"
    response = _http.get(url, headers={"x-api-key": _config.api_key}, params={"include_counts": include_counts})
    attributes = _check_response(response)
    return attributes


@_check_url_base
def get_node_ids(coll_type: str) -> _Any:
    """Returns a list of node identifiers in NeDRex for the given type

    Parameters
    ----------
    coll_type: str
        The node type to get IDs for

    Returns
    -------
    node_ids: list[str]
        The list of available node IDs for the specificed node type
    """
    _check_type(coll_type, "node")

    url: str = f"{_config.url_base}/{coll_type}/attributes/primaryDomainId/json"

    resp = _http.get(url, headers={"x-api-key": _config.api_key})
    data = _check_response(resp)
    node_ids = [i["primaryDomainId"] for i in data]
    return node_ids


@_check_url_base
def get_nodes(
    node_type: str,
    attributes: _Optional[_List[str]] = None,
    node_ids: _Optional[_List[str]] = None,
    limit: _Optional[int] = None,
    offset: int = 0,
) -> _Any:
    """Returns nodes in NeDRex of the given type

    Parameters
    ----------
    node_type : str
        The node type to collect
    attributes : list[str], optional
        A list of attributes to return for the collected nodes. The
        default, None, returns all attributes.
    node_ids : list[str], optional
        A list of IDs of specific nodes to be returned. The default (None)
        does no filtering by node ID.
    limit : int, optional
        A limit for the number of records to be returned. The default is
        determined by querying the API.
    offset : int, optional
        The number of records to skip before returning records. Default is
        0 (no records skipped).

    Returns
    -------
    items : list[dict[str, Any]]
        The nodes in NeDRex returned by the API.
    """
    _check_type(node_type, "node")

    upper_limit = _get_pagination_limit()
    _check_pagination_limit(limit, upper_limit)

    params = {"node_id": node_ids, "attribute": attributes, "offset": offset, "limit": limit}

    resp = _http.get(
        f"{_config.url_base}/{node_type}/attributes/json", params=params, headers={"x-api-key": _config.api_key}
    )

    items = _check_response(resp)
    return items


@_check_url_base
def iter_nodes(
    node_type: str, attributes: _Optional[_List[str]] = None, node_ids: _Optional[_List[str]] = None
) -> _Generator[_Dict[str, _Any], None, None]:
    """A function that returns a generator to iterate over nodes

    This function is useful if you wish to get all nodes in a particular
    collection, but do not want to manually handle offsets and limits.

    Parameters
    ----------
    node_type : str
        The node type to collect
    attributes : list[str], optional
        A list of attributes to return for the collected nodes. The
        default, None, returns all attributes.
    node_ids : list[str], optional
        A list of IDs of specific nodes to be returned. The default (None)
        does no filtering by node ID.


    Yields
    ------
    doc : dict[str, Any]
        A node in NeDRex returned by the API
    """

    _check_type(node_type, "node")
    upper_limit = _get_pagination_limit()

    params: _Dict[str, _Any] = {"node_id": node_ids, "attribute": attributes, "limit": upper_limit}

    offset = 0
    while True:
        params["offset"] = offset
        resp = _http.get(
            f"{_config.url_base}/{node_type}/attributes/json", params=params, headers={"x-api-key": _config.api_key}
        )

        data = _check_response(resp)

        for doc in data:
            yield doc

        if len(data) < upper_limit:
            break
        offset += upper_limit


@_check_url_base
def get_edges(edge_type: str, limit: _Optional[int] = None, offset: _Optional[int] = None) -> _Any:
    """
    Returns edges in NeDRex of the given type

    Parameters
    ----------
    edge_type : str
        The edge type to collect
    limit : int, optional
        A limit for the number of records to be returned. The default is
        determined by querying the API.
    offset : int, optional
        The number of records to skip before returning records. Default is
        0 (no records skipped).

    Returns
    -------
    items : list[dict[str, Any]]
        The edges in NeDRex returned by the API.
    """
    _check_type(edge_type, "edge")

    params = {"limit": limit, "offset": offset, "api_key": _config.api_key}

    resp = _http.get(f"{_config.url_base}/{edge_type}/all", params=params, headers={"x-api-key": _config.api_key})
    items = _check_response(resp)
    return items


@_check_url_base
def iter_edges(edge_type: str) -> _Generator[_Dict[str, _Any], None, None]:
    """A function that returns a generator to iterate over edges

    This function is useful if you wish to get all edges in a particular
    collection, but do not want to manually handle offsets and limits.

    Parameters
    ----------
    edge_type : str
        The edge type to collect

    Yields
    ------
    doc : dict[str, Any]
        An edge in NeDRex returned by the API
    """
    _check_type(edge_type, "edge")
    upper_limit = _get_pagination_limit()

    offset = 0
    while True:
        params = {"offset": offset, "limit": upper_limit}
        resp = _http.get(f"{_config.url_base}/{edge_type}/all", params=params, headers={"x-api-key": _config.api_key})
        data = _check_response(resp)

        for doc in data:
            yield doc

        if len(data) < upper_limit:
            break
        offset += upper_limit
