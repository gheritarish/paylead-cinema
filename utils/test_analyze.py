import geopandas as gpd
import pytest
from analyze import analyze_network, biggest_networks, cinemas_in_town


@pytest.fixture
def data_definition_test():
    data = gpd.read_file("./data.geojson")
    return data


def test_count_exact_number_of_theaters_in_paris(data_definition_test):
    data = data_definition_test
    number_theaters_paris = cinemas_in_town(data, "Paris")
    try:
        assert number_theaters_paris == 90
    except Exception as error:
        pytest.fail(f"Failed to count the number of theaters in Paris. Error: {error}.")


def test_count_no_theaters_in_amilly(data_definition_test):
    data = data_definition_test
    number_theaters_amilly = cinemas_in_town(data, "Amilly")
    try:
        assert number_theaters_amilly == 0
    except Exception as error:
        pytest.fail(f"Failed to count 0 theaters in Amilly. Error: {error}.")


def test_biggest_network_negative_argument(data_definition_test):
    data = data_definition_test
    with pytest.raises(ValueError):
        assert biggest_networks(data, -1)


def test_biggest_network_good_length(data_definition_test):
    data = data_definition_test
    four_biggest_networks = biggest_networks(data, 4)
    try:
        assert len(four_biggest_networks) == 4
    except Exception as error:
        pytest.fail(f"Failed to limit to 4 networks. Error: {error}.")


def test_analyze_unexisting_network(data_definition_test):
    data = data_definition_test
    with pytest.raises(ValueError):
        assert analyze_network(data, "Alakazam-the-theaters")


def test_analyze_existing_network(data_definition_test):
    data = data_definition_test
    network_analysis = analyze_network(data, "UGC")
    try:
        assert len(network_analysis) == 5
        assert type(network_analysis) is list
    except Exception as error:
        pytest.fail(f"Failed to find 5 arguments. Error: {error}.")
