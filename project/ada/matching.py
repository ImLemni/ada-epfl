import re
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


def normalize_title(title):
    """
    Normalizes the title by removing punctuation, extra spaces and parenthesized groups
    """
    title = title.lower()
    # title = sub("\((.*film.*|.*movie.*)\)", "", title)
    title = re.sub(r"\(.*\)", "", title)  # Remove parenthesized groups
    title = re.sub(r"\s+", " ", title)  # Replace consecutive whitespaces by a single space
    title = title.strip()
    title = re.sub(r"(?:[\[\](),.!?;:]|dvd|vhs)", "", title)  # Remove punctuation
    return title


def group_meta_by_title(entries, raw_titles):
    """
    Returns a dictionary from normalized titles (`str`) to lists of matching metadata.
    It keeps only the entries with a title matching one of those in `raw_titles`:
    `raw_titles` acts as a filter.
    """
    result = {}
    cleaned_titles = set()
    for raw_title in raw_titles:
        cleaned_titles.add(normalize_title(raw_title))

    for entry in entries:
        if "title" not in entry:
            continue
        cleaned_title = normalize_title(entry["title"])
        if cleaned_title not in cleaned_titles:
            continue

        if cleaned_title not in result:
            result[cleaned_title] = []
        result[cleaned_title].append(entry)

    return result


# def add_franchise_id(df, franchise_dict):
#     df['franchise_id']=df['asin'].apply(lambda x: franchise_dict[x])
#     return df
#
# wiki_dict, books_match, movies_match = filterData.get_matching_product()
#
#
# product_to_franchise = {}
# franchise_id = 0
# for k, v in wiki_dict.items():
#     associate = False
#     if clean_title(k) in books_match and len(books_match[clean_title(k)]) > 0:
#         for mov in v:
#             if clean_title(mov) in movies_match and len(movies_match[clean_title(mov)]) > 0:
#                 associate = True
#                 for movie_product in movies_match[clean_title(mov)]:
#                     product_to_franchise[movie_product['asin']] = franchise_id
#         for book_product in books_match[clean_title(k)]:
#             product_to_franchise[book_product['asin']] = franchise_id
#     franchise_id += 1 if associate else 0
#
#


if __name__ == "__main__":
    print(get_wikipedia_matching())
