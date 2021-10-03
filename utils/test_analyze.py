import geopandas as gpd
import pytest
from analyze import cinemas_in_town


def test_count_exact_number_of_theaters_in_paris():
    data = gpd.read_file("./data.geojson")
    number_theaters_paris = cinemas_in_town(data, "Paris")
    try:
        assert number_theaters_paris == 90
    except Exception as error:
        pytest.fail(f"Failed to count the number of theaters in Paris. Error: {error}.")


def test_count_no_theaters_in_amilly():
    data = gpd.read_file("./data.geojson")
    number_theaters_amilly = cinemas_in_town(data, "Amilly")
    try:
        assert number_theaters_amilly == 0
    except Exception as error:
        pytest.fail(f"Failed to count 0 theaters in Amilly. Error: {error}.")
