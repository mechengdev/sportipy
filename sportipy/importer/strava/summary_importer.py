from __future__ import annotations

from typing import Sequence
from pathlib import Path

import pandas as pd
from sportipy.importer.utils import gpx_to_dataframe, unzip_gz, fit_to_gpx


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

        If given activity Filename is `.fit` or `.fit.gz`, it will be converted into GPX file
        and added to the `activities` directory. The conversion for each activity file will happen
        only once and in the case of multiple encountered `.fit` files, it might take some time.

        Returns:
            A mapping, where keys are activity filenames and values corresponding DataFrames.
        """
        activities = self.load_activities()
        activities = activities[activities["Activity ID"].isin(list(activity_id))]
        found_as_gpx = set()
        for activity_file in activities["Filename"]:
            if pd.isna(activity_file):
                continue
            fullpath: Path = self._path / activity_file
            # TODO: .fit to .gpx conversion takes a long time for many files
            if fullpath.suffixes == [".fit", ".gz"]:
                maybe_gpx = Path(str(fullpath).replace(".fit.gz", ".gpx"))
                if maybe_gpx.exists():
                    found_as_gpx.add(str(maybe_gpx))
                    continue
                path_fit = unzip_gz(str(fullpath))
                as_gpx = path_fit.replace(".fit", ".gpx")
                fit_to_gpx(in_=path_fit, out_=as_gpx)
                found_as_gpx.add(as_gpx)
            elif fullpath.suffix == ".gpx":
                found_as_gpx.add(str(fullpath))
        return {x: df for x, df in gpx_to_dataframe(list(found_as_gpx)).items()}
