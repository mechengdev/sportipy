from __future__ import annotations

from typing import Sequence
from pathlib import Path

import pandas as pd
from sportipy.importer.utils import gpx_to_dataframe


class StravaSummaryImporter:
    """Importer for Strava summary file directory.
    
    For more information on how to bulk export your Strava data can be found at: https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#h_01GG58HC4F1BGQ9PQZZVANN6WF

    Args:
        path: Path to the unzipped Strava summary folder.
    """
    def __init__(self, path: str) -> None:
        self._path = Path(path)

    @property
    def path(self) -> str:
        return str(self._path)

    def load_activities(self) -> pd.DataFrame:
        return pd.read_csv(self._path / "activities.csv")

    def load_gpx(self, activity_id: str | int | Sequence[str, int]) -> dict[str, pd.DataFrame]:
        """Load GPX files of the given activities.

        Returns:
            A mapping, where keys are activity IDs and values corresponding DataFrames.
        """
        # TODO: Handle .fit files
        gpx_dir = self._path / "activities"
        # Pick matching .gpx files
        lookup = set(list(activity_id))
        id_to_file = {}
        for gpx in gpx_dir.glob("*.gpx"):
            if int(gpx.stem) in lookup:
                id_to_file[gpx] = gpx_dir / gpx
        return {Path(x).parts[-1].replace(".gpx", ""): df for x, df in gpx_to_dataframe(id_to_file.values()).items()}
