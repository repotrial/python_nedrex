import os
from typing import Optional

import requests  # type: ignore

from python_nedrex import config
from python_nedrex.decorators import check_url_vpd


@check_url_vpd
def get_vpd(disorder: str, number_of_patients: int, out_dir: str) -> Optional[str]:
    """
    Downloads a .zip archive with the requested virtual patient data to the given directory.

        Parameters:
            disorder (str): The disorder mondoID (e.g mondo.0000090) for which the virtual patient should be retrieved.
            number_of_patients (int): The number of simulated patients in the dataset. Can be 1, 10 or 100.
            out_dir (str): The absolute path of a directory where the virtual patient data should be stored.

        Returns:
            archive (str): Absolute path of the downloaded zip archive or None if the requested resource does not exist.
    """
    archive_name: str = f"{disorder}_1000GP_{number_of_patients}VPSim.zip"
    url: str = f"{config.url_vpd}/vpd/{disorder}/{archive_name}"
    archive: str = os.path.join(out_dir, archive_name)

    data = requests.get(url)
    if data.status_code != 200:
        return None

    with open(archive, "wb") as arch:
        arch.write(data.content)
    return archive
