"""Module containing python functions to access the disorder routes in the NeDRex API"""

from typing import Any, Callable, List, Union

import requests  # type: ignore

from python_nedrex import config
from python_nedrex.decorators import check_url_base


def _generate_route(path: str) -> Callable[[Union[str, List[str]]], Any]:
    @check_url_base
    def new_func(codes: Union[str, List[str]]) -> Any:
        if isinstance(codes, str):
            codes = [codes]

        url = f"{config.url_base}/disorder/{path}"
        resp = requests.get(url, params={"q": codes}, headers={"x-api-key": config.api_key})
        return resp.json()

    return new_func


search_by_icd10 = _generate_route("get_by_icd10")
get_disorder_descendants = _generate_route("descendants")
get_disorder_ancestors = _generate_route("anscestors")
get_disorder_parents = _generate_route("parents")
get_disorder_children = _generate_route("children")
