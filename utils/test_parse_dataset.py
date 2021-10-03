import geopandas as gpd
import pytest
from parse_dataset import parse_dataset


def test_parse_dataset_if_no_file_exists():
    dataset = parse_dataset("./file.geojson")
    try:
        assert type(dataset) is gpd.GeoDataFrame
    except Exception as error:
        pytest.fail(f"Fail to assert the type to a GeoDataFrame. Error: {error}.")


def test_parse_dataset_not_empty():
    dataset = parse_dataset("./data.geojson")
    try:
        assert type(dataset) is gpd.GeoDataFrame
        assert dataset.shape[0] > 0
    except Exception as error:
        pytest.fail(f"Fail to create a non-empty GeoDataFrame. Error: {error}.")
