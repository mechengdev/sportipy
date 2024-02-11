from __future__ import annotations

from typing import Sequence
import concurrent.futures

import pandas as pd
import gpxpy

from sportipy.utils import ms_to_min_per_km


def gpxpy_to_dataframe(gpx: gpxpy.mod_gpx.GPX) -> pd.DataFrame:
    """Convert gpxpy object to a pandas DataFrame.

    Speed is calculated between two points if it does not exists in the object.
    """
    df_dicts = []
    for track in gpx.tracks:
        for segment in track.segments:
            for idx, point in enumerate(segment.points):
                if point.speed is None:
                    if idx == 0:
                        speed = None
                    else:
                        speed = 0
                        speed_between = point.speed_between(segment.points[idx - 1])
                        if speed_between:
                            speed = ms_to_min_per_km(speed_between)
                else:
                    speed = point.speed
                df_dicts.append(
                    {
                        "lat": point.latitude,
                        "lon": point.longitude,
                        "elev": point.elevation,
                        "time": point.time,
                        "speed": speed
                    }
                )
    return pd.DataFrame(df_dicts)


def gpx_to_dataframe(filepath: str | Sequence[str]) -> dict[str, pd.DataFrame]:
    """Convert GPX file to a pandas DataFrame.
    
    Returns:
        A mapping, where keys are filepaths and values corresponding DataFrames.
    """
    results = {}

    def read_and_convert_to_dataframe(path):
        with open(path, "r") as f:
            # TODO: Something is blocking
            gpx = gpxpy.parse(f)
        results[path] = gpxpy_to_dataframe(gpx)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(read_and_convert_to_dataframe, path) for path in list(filepath)]
    [future.result() for future in concurrent.futures.as_completed(futures)]
    return results
