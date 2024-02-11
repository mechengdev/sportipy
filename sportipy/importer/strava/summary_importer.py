from __future__ import annotations

from pathlib import Path

import pandas as pd


class StravaSummaryImporter:
    """Importer for Strava summary file directory.
    
    For more information on how to bulk export your Strava data can be found at: https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#h_01GG58HC4F1BGQ9PQZZVANN6WF

    Args:
        path: Path to the unzipped Strava summary folder.
    """
    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def path(self):
        return self._path

    def load_activities(self) -> pd.DataFrame:
        return pd.read_csv(Path(self._path) / "activities.csv")
