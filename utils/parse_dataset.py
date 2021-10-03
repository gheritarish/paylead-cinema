import re
from zipfile import ZipFile, ZipInfo

import geopandas as gpd
from loguru import logger


def find_geojson_file_in_zip(zip_file: str) -> str:
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
        logger.warning(
            f"Several files have a corresponding name: {len(geojson_files)} files."
        )


def extract_geojson_file(geojson_file: ZipInfo, zip_file: str) -> str:
    with ZipFile(zip_file, "r") as file_zip:
        file_zip.extract(member=geojson_file)
        return geojson_file.filename


def parse_dataset(geojson_path: str) -> gpd.GeoDataFrame:
    try:
        cinema_data = gpd.read_file(geojson_path)
        return cinema_data
    except Exception as error:
        logger.warning(error)
        return gpd.GeoDataFrame()
