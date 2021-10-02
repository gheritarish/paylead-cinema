from loguru import logger

from utils.get_data import download_from_url, find_url, get_url_from_site


def main():
    url_raw = get_url_from_site(
        site_url="https://www.data.gouv.fr/fr/datasets/cinemas-issus-dopenstreetmap/"
    )
    list_url = find_url(url_raw)
    for url in list_url:
        name = str(url.split("/")[-1])
        logger.info(name)
        download_from_url(url=url, save_path=name)


if __name__ == "__main__":
    main()
