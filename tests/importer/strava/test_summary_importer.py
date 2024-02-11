import pytest
from pathlib import Path

from sportipy.importer.strava.summary_importer import StravaSummaryImporter


BULK_EXPORT_DIR = Path(__file__).parent / "resources/export_123"


@pytest.fixture
def importer():
    return StravaSummaryImporter(BULK_EXPORT_DIR)


def test_init(importer):
    assert importer.path == str(BULK_EXPORT_DIR)


def test_load_activities(importer):
    df = importer.load_activities()
    assert len(df) == 2


def test_load_gpx(importer):
    activities = importer.load_activities()
    gpxs = importer.load_gpx(activities[activities["Activity Type"] == "Run"]["Activity ID"].values)
    assert len(gpxs) == len(activities)
