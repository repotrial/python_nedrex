"""Top-level package for python-nedrex."""

__author__ = """David James Skelton"""
__email__ = "james.skelton@newcastle.ac.uk"
__version__ = "0.1.0"

from dataclasses import dataclass
from typing import Optional


@dataclass
class _Config:
    _url_base: Optional[str] = None
    _url_vpd: Optional[str] = None
    _api_key: Optional[str] = None


config: _Config = _Config()


def set_url_base(url_base: str) -> None:
    config._url_base = url_base.rstrip("/")

def set_url_vpd(url_vpd: str)-> None:
    config._url_vpd = url_vpd.rstrip("/")

def set_api_key(key: str) -> None:
    config._api_key = key
