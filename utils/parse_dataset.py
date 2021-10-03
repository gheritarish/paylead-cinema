import re
from zipfile import ZipFile, ZipInfo

import geopandas as gpd
from loguru import logger


def find_geojson_file_in_zip(zip_file: str) -> ZipInfo:
    """Function to find the geojson file in a given zip file.

    Args:
        zip_file (str): The path to the zip file.

    Returns:
        (ZipInfo) The geojson file in the archive, as a ZipInfo object.

    Raises:
        Exception: This exception is raised if there are several files corresponding.
    """
    with ZipFile(zip_file, "r") as file_zip:
        geojson_file = re.compile(r"^[\w-]+\.geojson$")
        # zip_members = file_zip.namelist()
        zip_members = file_zip.infolist()
        geojson_files = [
            file for file in zip_members if geojson_file.match(file.filename)
        ]
    if len(geojson_files) == 1:
        return geojson_files[0]
    else:
        raise Exception("Several files correspond to the given regex.")


def extract_geojson_file(geojson_file: ZipInfo, zip_file: str) -> str:
    """Function to extract a geojson file from a zip archive.

    Args:
        geojson_file (ZipInfo): The geojson file to extract, as a ZipInfo object.
        zip_file (str): The path to the zip file.

    Returns:
        (str): The path to the extracted file.

    """
    with ZipFile(zip_file, "r") as file_zip:
        file_zip.extract(member=geojson_file)
        return geojson_file.filename


def parse_dataset(geojson_path: str) -> gpd.GeoDataFrame:
    """Function to create a GeoDataFrame from a given geojson file.

    Args:
        geojson_path (str): The path to the geojson file.

    Returns:
        (gpd.GeoDataFrame) The GeoDataFrame constructed by reading the geojson file.

    """
    try:
        cinema_data = gpd.read_file(geojson_path)
        return cinema_data
    except Exception as error:
        logger.warning(error)
        return gpd.GeoDataFrame()
