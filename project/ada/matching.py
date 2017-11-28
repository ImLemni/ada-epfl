import requests
from bs4 import BeautifulSoup

from ada.progressbar import ProgressBar

WIKIPEDIA_LISTS = [
    "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(0%E2%80%939_and_A%E2%80%93C)",
    "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(D%E2%80%93J)",
    "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(K%E2%80%93R)",
    "https://en.wikipedia.org/wiki/List_of_fiction_works_made_into_feature_films_(S%E2%80%93Z)",
]


def get_wikipedia_matching():
    """
    Returns a dictionary matching book names (`str`) to movies (`List[str]`) according to Wikipedia.

    :return: Dictionary from book names to movie names.
    """
    result = {}
    with ProgressBar(len(WIKIPEDIA_LISTS)) as progress_bar:
        for wikipedia_list_url in WIKIPEDIA_LISTS:
            req = requests.get(wikipedia_list_url)
            current_matching = scrap_wikipedia_list(req.text)
            result = {**result, **current_matching}
            progress_bar.update(1)
    return result


def scrap_wikipedia_list(html: str):
    """
    Scraps a wiki page and returns a dictionary from book titles (`str`) to movie titles (`List[str]`)
    """
    result = {}
    soup = BeautifulSoup(html, "html5lib")
    for row in soup.select("table.wikitable tr"):
        cells = row.findAll("td")
        if len(cells) != 2:
            continue
        book_title: str = cells[0].find(text=True)
        movie_data = cells[1].findAll(text=True)
        movie_titles = [movie_data[0]]
        movie_titles_mult = [value for index, value in enumerate(movie_data) if
                             movie_data[(index - 1) % len(movie_data)] == '\n']
        result[book_title] = list(set(movie_titles + movie_titles_mult))
    return result
