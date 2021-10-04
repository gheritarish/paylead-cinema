import geopandas as gpd
import pandas as pd
from loguru import logger


def cinemas_in_town(data: gpd.GeoDataFrame, town_name: str) -> int:
    """Function to find the number of theaters in a town, given the town name.

    Args:
        data (gpd.GeoDataFrame): A GeoDataFrame with the theaters data.
        town_name (str): The name of the town of which we want the number of theaters.

    Returns:
        (int): The number of theaters in the given town.

    """
    data = data["com_nom"].value_counts()
    try:
        theaters_town = data[town_name]
        return theaters_town
    except Exception as error:
        logger.warning(error)
        return 0


def biggest_networks(data: gpd.GeoDataFrame, number_of_networks: int) -> pd.Series:
    """Function to get the biggest networks, by number of theaters.

    This function will limit itself to the number given by the user.

    Args:
        data (gpd.GeoDataFrame): A GeoDataFrame with the theaters data.
        number_of_networks (int): The number of biggest networks we want to get.

    Returns:
        (pd.Series) A series with the names of the network and their number of theaters.

    Raises:
        ValueError: This exception is raised if the number_of_network given is negative.
    """
    data = data["marque"].value_counts()
    if number_of_networks > 0:
        biggest_networks_numbers = data[:number_of_networks]
        return biggest_networks_numbers
    else:
        raise ValueError("The entered argument is negative")
        return pd.Series()


def analyze_network(data: gpd.GeoDataFrame, network_name: str):
    """Function to analyze a given network of theaters.

    This function gives the theater with the highest number of screens,
    the theater with the highest number of seats,
    and the number of theaters with available 3D projections.

    Args:
        data (gpd.GeoDataFrame): A GeoDataFrame with the theaters data.
        network_name (str): The name of the network to analyze.

    Returns:
        (List): A list with, in order: the name of the theater with the highest number
        of screens, and its number of screens; the name of the theater with the highest
        number of seats, and its number of seats; the number of theaters with available
        3D projection in the network.

    Raises:
        ValueError: This exception is raised if the network_name is unknown.
    """
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


def theaters_in_department(data: gpd.GeoDataFrame, code_department: str) -> int:
    data["department"] = data.com_insee.apply(
        lambda x: x[:3] if x[0] == "9" and int(x[1]) > 5 else x[:2]
    )
    data = data["department"].value_counts()
    try:
        return int(data[code_department])
    except Exception as error:
        logger.warning(error)
        return 0
