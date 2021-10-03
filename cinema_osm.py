#!./paylead/bin/python3.8

import argparse

from loguru import logger

from utils.analyze import cinemas_in_town
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
        help="Defines the mode of the script: initialize, extract or analyze",
    )
    parser.add_argument(
        "--theatersintown",
        type=str,
        help="Counts the number of theaters in a given town",
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
            logger.info(
                f"""There are {number_theaters_town} theaters in {args.theatersintown}."""
            )

    else:
        logger.error(
            "This mode doesn't exist. Available modes: initialize, extract or analyze"
        )


if __name__ == "__main__":
    main()
