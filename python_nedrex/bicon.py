from pathlib import Path
from typing import IO, Any, Dict, Optional

from python_nedrex import config
from python_nedrex.common import check_response, download_file, http


def bicon_request(
    expression_file: IO[str],
    lg_min: int = 10,
    lg_max: int = 15,
    network: str = "DEFAULT",
) -> str:
    files = {"expression_file": expression_file}
    data = {"lg_min": lg_min, "lg_max": lg_max, "network": network}

    url = f"{config.url_base}/bicon/submit"
    resp = http.post(url, data=data, files=files, headers={"x-api-key": config.api_key})
    result: str = check_response(resp)
    return result


def check_bicon_status(uid: str) -> Dict[str, Any]:
    url = f"{config.url_base}/bicon/status"
    resp = http.get(url, params={"uid": uid}, headers={"x-api-key": config.api_key})
    result: Dict[str, Any] = check_response(resp)
    return result


def download_bicon_data(uid: str, target: Optional[str] = None) -> None:
    if target is None:
        target = str(Path(f"{uid}.zip").resolve())

    url = f"{config.url_base}/bicon/download?uid={uid}"

    download_file(url, target)
