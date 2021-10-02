import pytest
import requests
import responses
from get_data import find_url


def test_if_find_url_returns_all_good_url():
    list_url = [
        "test.png",
        "https://geodatamine.fr/dump/file",
        "https://geodatamine.fr/dump/file.gz2",
        "https://geodatamine.fr/file_csv.zip",
        "https://geodatamine.fr/dump/file_csv.zip",
        "https://geodatamine.fr/dump/file_geojson.zip",
        "https://geodatamine.fr/dump/C1N3MAS_france_geojson.zip",
        "https://geodataminefr/dump/file/zip",
    ]
    try:
        result = find_url(list_url)
        assert type(result) is list
        assert result == [
            "https://geodatamine.fr/dump/file_geojson.zip",
            "https://geodatamine.fr/dump/C1N3MAS_france_geojson.zip",
        ]
    except Exception as error:
        pytest.fail(f"Failed to select only good url. Error: {error}.")


def test_if_fail_to_find_good_url():
    list_url = [
        "https://geodatamine.fr/dump/file_csv.zip",
        "https://geodatamine.fr/dump/file_geojson_2.zip",
        "https://geodatamine.fr/dump/geojson_file.zip",
    ]
    try:
        result = find_url(list_url)
        assert type(result) is list
        assert len(result) == 0
    except Exception as error:
        pytest.fail(f"Failed to dump all bad url. Error: {error}.")


def test_connection_to_site_for_scraping():
    responses.add(
        responses.GET,
        "https://www.data.gouv.fr/fr/datasets/cinemas-issus-dopenstreetmap/",
        status=200,
    )

    resp = requests.get(
        url="https://www.data.gouv.fr/fr/datasets/cinemas-issus-dopenstreetmap/"
    )
    assert resp.status_code == 200
