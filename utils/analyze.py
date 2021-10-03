from typing import List

import geopandas as gpd
from loguru import logger


def cinemas_in_town(data: gpd.GeoDataFrame, town_name: str) -> List[int]:
    data = data.groupby(["com_nom"], as_index=False).count()
    try:
        theaters_town = data[data.com_nom == town_name]
        number_theaters = theaters_town["osm_id"].values[0]
        return number_theaters
    except Exception as error:
        logger.warning(error)
        return 0
