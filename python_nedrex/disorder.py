from typing import Union

import requests

from python_nedrex import config
from python_nedrex.decorators import check_url_base


def _generate_route(path: str):
    @check_url_base
    def f(codes: Union[str, list[str]]):
        if isinstance(codes, str):
            codes = [codes]

        url = f"{config._url_base}/disorder/{path}"
        resp = requests.get(url, params={"q": codes})
        return resp.json()

    return f


search_by_icd10 = _generate_route("get_by_icd10")
get_disorder_descendants = _generate_route("descendants")
get_disorder_ancestors = _generate_route("anscestors")
get_disorder_parents = _generate_route("parents")
get_disorder_children = _generate_route("children")
