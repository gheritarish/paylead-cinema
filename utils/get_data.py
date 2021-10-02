import re
from typing import List

import requests
from bs4 import BeautifulSoup


def get_url_from_site(site_url: str) -> List[str]:
    """Function to get all URL from a given website, without any filtering.

    Args:
        site_url (str): The site URL from which to scrap the data.

    Returns:
        List[str]: The list of all links on the original page.

    """
    site_data = requests.get(url=site_url)
    site_data_links = BeautifulSoup(site_data.content, "html.parser")
    links_raw = site_data_links.find_all("a")
    url_raw = [str(link.get("href")) for link in links_raw]
    return url_raw


def download_from_url(url: str, save_path: str, chunk_size: int = 8192):
    """Function to download a file from a given URL.

    Args:
        url (str): The URL of the file to download.
        save_path (str): The path to the file on which to write the data.
        chunk_size (int): The size of each part of file download.

    Examples:

        >>> download_from_url(url="http://test.html/dog.zip", "data.zip")
        Write file contained in "http://test.html/dog.zip" in file "data.zip"

    """
    request_file = requests.get(url, stream=True)
    with open(save_path, "wb") as file:
        for chunk in request_file.iter_content(chunk_size=chunk_size):
            file.write(chunk)


def find_url(url_raw: List[str]) -> List[str]:
    """Function to find all URL matching a specific regex in a list of URL.

    Here, this function will fetch all URL beginning with:
    "https://geodatamine.fr/dump/" and continuing with "t3xt-4nd-numb3rs.text".
    This allows to fetch the direct URL of the files to download.

    Args:
        url_raw (str): The list of URL from which to find a corresponding URL.

    Returns:
        List[str]: The list of URL corresponding to the given format.

    """

    regex = re.compile(r"^https:\/\/geodatamine\.fr\/dump\/[\w-]+geojson\.[A-Za-z]+$")
    url = [str(link) for link in url_raw if regex.match(str(link))]
    return url
