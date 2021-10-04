#!./paylead/bin/python3.8

import argparse

from loguru import logger

from utils.analyze import (
    analyze_network,
    biggest_networks,
    cinemas_in_town,
    theaters_in_department,
)
from utils.get_data import download_from_url, find_url, get_url_from_site
from utils.parse_dataset import (
    extract_geojson_file,
    find_geojson_file_in_zip,
    parse_dataset,
)


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        help="Defines the mode of the script: initialize or analyze",
    )
    parser.add_argument(
        "--theatersintown",
        type=str,
        help="Counts the number of theaters in a given town",
        default=None,
    )
    parser.add_argument(
        "--biggestnetworks",
        type=int,
        help="Gives the number of theaters for the number of biggest networks given",
        default=None,
    )
    parser.add_argument(
        "--analyzenetwork",
        type=str,
        help="For a given network name, returns the theater with the highest number of screens, the highest number of seats, and the number of 3D theaters",
        default=None,
    )
    parser.add_argument(
        "--theatersindepartment",
        type=str,
        help="The code of a department",
        default=None,
    )
    args = parser.parse_args()
    return args


def main():
    args = define_args()

    if args.mode == "initialize":
        url_raw = get_url_from_site(
            site_url="https://www.data.gouv.fr/fr/datasets/cinemas-issus-dopenstreetmap/"
        )
        list_url = find_url(url_raw)
        for url in list_url:
            name = str(url.split("/")[-1])
            logger.info(name)
            download_from_url(url=url, save_path=name)
    elif args.mode == "analyze":
        member_file = find_geojson_file_in_zip("./cinema_geojson.zip")
        geojson_extracted_path = extract_geojson_file(
            geojson_file=member_file, zip_file="./cinema_geojson.zip"
        )
        cinema_gdf = parse_dataset(geojson_path=geojson_extracted_path)

        if args.theatersintown:
            number_theaters_town = cinemas_in_town(
                cinema_gdf, town_name=args.theatersintown
            )
            print(
                f"""There are {number_theaters_town} theaters in {args.theatersintown}."""
            )

        if args.biggestnetworks:
            try:
                theaters_biggest_networks = biggest_networks(
                    data=cinema_gdf, number_of_networks=args.biggestnetworks
                )
                # print(theaters_biggest_networks)
                for index in range(len(theaters_biggest_networks)):
                    print(
                        theaters_biggest_networks.index[index]
                        + ": "
                        + str(theaters_biggest_networks[index])
                        + " theaters."
                    )
            except Exception as error:
                logger.warning(error)

        if args.analyzenetwork:
            try:
                network_analysis = analyze_network(
                    data=cinema_gdf, network_name=args.analyzenetwork
                )
                # if network_analysis:
                print(
                    f"""Network: {args.analyzenetwork}:\n
Highest number of screens: {network_analysis[1]} at {network_analysis[0]}\n
Biggest theater: {network_analysis[2]} seats at {network_analysis[3]}\n
{network_analysis[4]} 3D theaters in this network."""
                )
            except Exception as error:
                logger.warning(error)

        if args.theatersindepartment:
            try:
                number_theaters = theaters_in_department(
                    data=cinema_gdf, code_department=args.theatersindepartment
                )
                print(
                    f"""There are {number_theaters} theaters in department {args.theatersindepartment}"""
                )
            except Exception as error:
                logger.warning(error)
    else:
        logger.error("This mode doesn't exist. Available modes: initialize or analyze")


if __name__ == "__main__":
    main()
