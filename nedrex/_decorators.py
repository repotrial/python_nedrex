from functools import wraps
from typing import Any, Callable, TypeVar

from nedrex import config
from nedrex.exceptions import ConfigError

R = TypeVar("R")


def check_url_base(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def wrapped_fx(*args: Any, **kwargs: Any) -> Any:
        if hasattr(config, "url_base") and config.url_base is not None:
            return func(*args, **kwargs)
        raise ConfigError("API URL is not set in the config")

    return wrapped_fx


def check_url_vpd(func: Callable[..., R]) -> Callable[..., R]:
    @wraps(func)
    def wrapped_fx(*args: Any, **kwargs: Any) -> Any:
        if hasattr(config, "url_vpd") and config.url_vpd is not None:
            return func(*args, **kwargs)
        raise ConfigError("VPD URL is not set in the config")

    return wrapped_fx
