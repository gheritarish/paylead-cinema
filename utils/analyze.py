from typing import List

import geopandas as gpd
import pandas as pd
from loguru import logger


def cinemas_in_town(data: gpd.GeoDataFrame, town_name: str) -> int:
    data = data["com_nom"].value_counts()
    try:
        theaters_town = data[town_name]
        return theaters_town
    except Exception as error:
        logger.warning(error)
        return 0


def biggest_networks(data: gpd.GeoDataFrame, number_of_networks: int) -> pd.Series:
    data = data["marque"].value_counts()
    if number_of_networks > 0:
        biggest_networks_numbers = data[:number_of_networks]
        return biggest_networks_numbers
    else:
        raise ValueError("The entered argument is negative")
        return pd.Series()


def analyze_network(data: gpd.GeoDataFrame, network_name: str):
    data = data[data["marque"] == network_name]
    if len(data) > 0:
        max_screens = data["nb_screens"][data["nb_screens"].notnull()].astype(int).max()
        name_theater_max_screens = data[["name"]][
            data.nb_screens == str(max_screens)
        ].values[0][0]
        max_seats = data["capacity"][data["capacity"].notnull()].astype(int).max()
        name_theater_max_seats = data[["name"]][data.capacity == str(max_seats)].values[
            0
        ][0]
        number_3d_theaters = data["cinema3d"][data["cinema3d"] == "yes"].count()
        return [
            name_theater_max_screens,
            max_screens,
            max_seats,
            name_theater_max_seats,
            number_3d_theaters,
        ]
    else:
        raise ValueError("No data for this network of theaters")
        return []
