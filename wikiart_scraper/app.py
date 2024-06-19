from __future__ import unicode_literals
from dataclasses import dataclass

import requests
import json
import os

from bs4 import BeautifulSoup

from prompt_toolkit.shortcuts import radiolist_dialog, checkboxlist_dialog, input_dialog

session = requests.Session()


@dataclass
class Artist:
    """
    A single search result for an artist on WikiArt.
    """

    name: str
    url: str


@dataclass
class Artwork:
    """
    A single artwork on WikiArt.
    """

    artist: Artist
    title: str
    year: str
    img: str


def search_for_artist(query: str) -> list[Artist]:
    """
    Return a list of ArtistSearchResult objects for the given query.
    """
    artist_encoded = query.replace(" ", "%20")

    search_results = requests.get(
        "https://www.wikiart.org/en/Search/" + artist_encoded, {"json": 3}, timeout=500
    )

    data = json.loads(search_results.text)

    artists_html = data["ArtistsHtml"]
    soup = BeautifulSoup(artists_html, "html.parser")

    artist_lis = soup.find_all("li", class_="title")
    artist_links = [li.find("a") for li in artist_lis]

    return [Artist(link.text, link["href"]) for link in artist_links]


def prompt_for_artist(query: str) -> Artist:
    """
    Prompt the user to select an artist from the search results for the given query.
    """
    search_results = search_for_artist(query)

    # return radiolist_prompt(
    #     title="Select an artist",
    #     values=[(artist, artist.name) for artist in search_results],
    # )

    return radiolist_dialog(
        title="Select an artist",
        values=[(artist, artist.name) for artist in search_results],
    ).run()


def get_artist_paintings(artist):
    # Fetch HTML content of the artist's page (replace with actual URL)
    artist_page_url = "https://www.wikiart.org" + artist.url
    response = requests.get(artist_page_url, timeout=500)
    artist_page_html = response.text

    # Parse the artist's page HTML
    soup = BeautifulSoup(artist_page_html, "html.parser")

    # get lis in wiki-masonry-container
    ul = soup.find("ul", class_="wiki-masonry-container")
    lis = ul.find_all("li")

    # Find the div with the painting data
    # painting_data_div = soup.find("div", ng_cloak=True, ng_controller="MasonryCtrl")

    paintings = []  # Create an empty list to store ArtistPainting objects

    for li in lis:
        img = li.find("img")
        title = li.find("a", class_="artwork-name").text
        year = li.find("span", class_="artwork-year").text
        paintings.append(Artwork(artist, title, year, img["src"]))

    return paintings


def prompt_for_paintings(artist_url):
    """
    Prompt the user to select a painting from the artist's page.
    """
    paintings = get_artist_paintings(artist_url)

    selected_paintings = checkboxlist_dialog(
        title="Select paintings",
        values=[(painting, painting.title) for painting in paintings],
        default_values=paintings,
    ).run()

    return selected_paintings


def kebabify_name(name):
    # remove non-alphanumeric characters
    name = "".join(char for char in name if char.isalnum() or char in [" ", "-"])

    # remove extra spaces
    name = " ".join(name.split()).strip()

    name = name.lower().replace(" ", "-")

    return name


def download_paintings(paintings):
    """
    Download the selected paintings to the local filesystem.

    - Images should be downloaded to a folder: "{artist_name}/{artist_name} - {painting_title} - {year}.jpg"
    - If artist name is missing, use "UKA" instead.
    - If year is missing, use "UKD" instead.
    """

    # make {artist_name} folder if it doesn't exist
    artist_name = paintings[0].artist.name

    print("Making directory: ", artist_name)

    for painting in paintings:
        painting_file = f"{kebabify_name(artist_name)}/{artist_name} - {painting.title} - {painting.year}.jpg"

        # if file has "!PinterestSmall.jpg" suffxed, remove it
        painting_file = painting_file.replace(".jpg!PinterestSmall.jpg", ".jpg")

        print(f"Downloading to {painting_file}")

        response = requests.get(painting.img, timeout=500)
        # Create the folder if it doesn't exist
        os.makedirs(os.path.dirname(painting_file), exist_ok=True)

        with open(painting_file, "wb") as file:
            file.write(response.content)


def main():
    # ask for artists name:
    # artist = input("Enter artist name: ")
    artist_name = input_dialog(
        title="Enter artist name", text="Enter artist name:"
    ).run()
    artist = prompt_for_artist(artist_name)
    paintings = prompt_for_paintings(artist)

    download_paintings(paintings)
