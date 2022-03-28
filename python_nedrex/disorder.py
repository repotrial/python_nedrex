from typing import Union

import requests

from python_nedrex import config
from python_nedrex.decorators import check_url_base

def generate_route(path: str):
    def f(codes: Union[str, list[str]]):
        if isinstance(codes, str):
            codes = [codes]
        
        url = f"{config._url_base}/disorder/{path}"
        resp = requests.get(url, params={"q": codes})
        return resp.json()        


@check_url_base
def search_by_icd10(codes: Union[str, list[str]]):
    if isinstance(codes, str):
        codes = [codes]
    
    url = f"{config._url_base}/disorder/get_by_icd10"
    resp = requests.get(url, params={"q": codes})
    return resp.json()


@check_url_base
def get_disorder_descendants(codes: Union[str, list[str]]):
    if isinstance(codes, str):
        codes = [codes]
    
    url = f"{config._url_base}/disorder/descendants"
    resp = requests.get(url, params={"q": codes})
    return resp.json()


@check_url_base
def get_disorder_ancestors(codes: Union[str, list[str]]):
    if isinstance(codes, str):
        codes = [codes]
    
    url = f"{config._url_base}/disorder/ancestors"
    resp = requests.get(url, params={"q": codes})
    return resp.json()


@check_url_base
def get_disorder_parents(codes: Union[str, list[str]]):
    if isinstance(codes, str):
        codes = [codes]
    
    url = f"{config._url_base}/disorder/parents"
    resp = requests.get(url, params={"q": codes})
    return resp.json()


@check_url_base
def get_disorder_children(codes: Union[str, list[str]]):
    if isinstance(codes, str):
        codes = [codes]
    
    url = f"{config._url_base}/disorder/children"
    resp = requests.get(url, params={"q": codes})
    return resp.json()
