# -*- coding: utf-8 -*-
"""Module containing a function providing access to Neo4j NeDRex
"""

import json as _json
from typing import Any as _Any
from typing import Dict as _Dict
from typing import Generator as _Generator
from typing import List as _List

from requests.exceptions import ChunkedEncodingError  # type: ignore

from nedrex import config as _config
from nedrex.common import http as _http
from nedrex.exceptions import NeDRexError


def neo4j_query(query: str) -> _Generator[_List[_Dict[str, _Any]], None, None]:
    """Run a cypher query on a Neo4j NeDRex instance

    Parameters
    ----------
    query : str
        A valid cypher query

    Yields
    ------
    item : list[dict[str, Any]]
        An individual result from the cypher query.
    """
    url = f"{_config.url_base}/neo4j/query"
    params = {"query": query}

    resp = _http.get(url, params=params, headers={"x-api-key": _config.api_key}, stream=True)
    if resp.status_code != 200:
        raise NeDRexError("Querying Neo4j returned a non-200 status code.")

    try:
        for line in resp.iter_lines():
            data = _json.loads(line.decode())
            for item in data:
                yield item
    except ChunkedEncodingError as exc:
        raise NeDRexError("cypher query could not be executed") from exc
