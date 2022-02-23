from typing import Callable, TypeVar, cast

from python_nedrex import config
from python_nedrex.exceptions import ConfigError


TCallable = TypeVar("TCallable", bound=Callable)


def check_url_base(func: TCallable) -> TCallable:
    def wrapped_fx(*args, **kwargs):
        if hasattr(config, "_url_base"):
            return func(*args, **kwargs)
        else:
            raise ConfigError("API URL is not set in the config")

    return cast(TCallable, wrapped_fx)
