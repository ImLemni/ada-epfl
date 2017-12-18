import re
import requests
from bs4 import BeautifulSoup
import ada
from ada.progressbar import ProgressBar
import unidecode
from ada import data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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
    title = unidecode.unidecode(title)
    # title = sub("\((.*film.*|.*movie.*)\)", "", title)
    title = re.sub(r"\(.*?\)", "", title)  # Remove parenthesized groups
    title = re.sub(r"\{.*?\}", "", title)
    title = re.sub(r"\[.*?\]", "", title)
    title = re.sub(r"&lt.*?&gt", "", title)  # Remove bad encoding groups
    title = re.sub(r"(?:&amp|&lt|&gt|&quot)", "", title)  # Remove bad encoding
    # Replace consecutive whitespaces by a single space
    title = re.sub(r"\s+", " ", title)
    title = title.strip()
    title = re.sub(r"(?:[\[\](),.!?;:\-\&]|dvd|vhs)",
                   "", title)  # Remove punctuation
    title = re.sub(r"\s+", " ", title)
    title = title.strip()
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


book_title_to_movie_titles = ada.matching.get_wikipedia_matching()
book_titles = [*book_title_to_movie_titles.keys()]
movie_titles = [title for movie_titles in book_title_to_movie_titles.values()
                for title in movie_titles]


title_to_movie_metas = group_meta_by_title(ada.data.read_data(
    "meta_Movies_and_TV", 208321), movie_titles)
len(title_to_movie_metas)


title_to_book_metas = group_meta_by_title(
    ada.data.read_data("meta_Books", 2370585), book_titles)

matched_titles_count = len(title_to_book_metas)
matched_meta_count = sum(len(meta) for meta in title_to_book_metas.values())

print(f"Number of books from wikipedia : {len(book_titles)}")
print(f"Number of matched book titles: {matched_titles_count}")
print(f"Number of matched book metadata: {matched_meta_count}")


matched_book_titles = set()
matched_movie_titles = set()


for raw_book_title, raw_movie_titles in book_title_to_movie_titles.items():
    clean_book_title = normalize_title(raw_book_title)
    if clean_book_title not in title_to_book_metas:
        continue

    for raw_movie_title in raw_movie_titles:
        clean_movie_title = normalize_title(raw_movie_title)
        if clean_movie_title not in title_to_movie_metas:
            continue

        matched_movie_titles.add(clean_movie_title)
        matched_book_titles.add(clean_book_title)


print(f"Number of matched books: {len(matched_book_titles)}")
print(f"Number of matched movies: {len(matched_movie_titles)}")


def filter_dict_keys(base_dict, keys):
    """
    Creates a new dictionary by only keeping the properties in `keys`
    of the `base_dict` dictionary.
    """
    result = {}
    for key in base_dict.keys():
        if key in keys:
            result[key] = base_dict[key]
    return result


# Keep only the products of franchises in both categories
title_to_book_metas = filter_dict_keys(
    title_to_book_metas, matched_book_titles)
title_to_movie_metas = filter_dict_keys(
    title_to_movie_metas, matched_movie_titles)

asin_to_book_meta = {}
asin_to_movie_meta = {}

for books in title_to_book_metas.values():
    for book in books:
        asin_to_book_meta[book["asin"]] = book

for movies in title_to_movie_metas.values():
    for movie in movies:
        asin_to_movie_meta[movie["asin"]] = movie

print(f"We have {len(asin_to_movie_meta.keys())} distincts product for movies")
print(f"We have {len(asin_to_book_meta.keys())} distincts product for books")


def filter_by_asin(reviews, asin_whitelist):
    asin_whitelist = set(asin_whitelist)
    for review in reviews:
        if review["asin"] in asin_whitelist:
            yield review


book_reviews_df = pd.DataFrame.from_dict(filter_by_asin(
    data.read_data("reviews_Books", 22507155), asin_to_book_meta.keys()))
book_reviews_df.to_json(data.get_path(
    "filtered_Books_reviews", use_gzip=False), orient='records')
print(f"Number of book reviews after filtering by asin: {book_reviews_df.shape[0]}")
movie_reviews_df = pd.DataFrame.from_dict(filter_by_asin(
    data.read_data("reviews_Movies_and_TV", 4607047), asin_to_movie_meta.keys()))
movie_reviews_df.to_json(data.get_path(
    "filtered_Movies_reviews", use_gzip=False), orient='records')
print(f"Number of movie reviews after filtering by asin: {movie_reviews_df.shape[0]}")
book_metas_df = pd.DataFrame.from_dict(filter_by_asin(
    data.read_data("meta_Books", 2370585), asin_to_book_meta.keys()))
book_metas_df.to_json(data.get_path(
    "filtered_Books_meta", use_gzip=False), orient='records')
print(f"Number of book metadata after filtering by asin: {book_metas_df.shape[0]}")
movie_metas_df = pd.DataFrame.from_dict(filter_by_asin(
    data.read_data("meta_Movies_and_TV", 208321), asin_to_movie_meta.keys()))
movie_metas_df.to_json(data.get_path(
    "filtered_Movies_meta", use_gzip=False), orient='records')
print(f"Number of movie metadata after filtering by asin: {movie_metas_df.shape[0]}")
books_df = book_reviews_df.merge(book_metas_df, on="asin")
books_df.to_json(data.get_path("filtered_Books",
                               use_gzip=False), orient='records')
print(f"Number of books (reviews and metadata) after joining on asin: {books_df.shape[0]}")

book_metas_df = None
book_reviews_df = None


movies_df = pd.read_json(data.get_path(
    "filtered_Movies", use_gzip=False), orient='records')
books_df = pd.read_json(data.get_path(
    "filtered_Books", use_gzip=False), orient='records')


def clean_merged_df(df):
    columns_to_drop = ["reviewTime", "reviewerName",
                       "imUrl", "categories", "salesRank", "related"]
    for col_name in columns_to_drop:
        if col_name in df.columns:
            df.drop(col_name, axis=1, inplace=True)

    def map_helpful(x):
        if type(x) != list:
            return x
        score, total = x
        return float('nan') if total == 0 else score / total

    df["helpful"] = df['helpful'].apply(map_helpful)


clean_merged_df(movies_df)
movies_df.to_json("merged_clean_Movies.json", orient='records')
movies_df.head(5)


clean_merged_df(books_df)
books_df.to_json("merged_clean_Books.json", orient='records')
books_df.head(5)

asin_to_franchise_id = {}
franchise_id = 0

for raw_book_title, raw_movie_titles in book_title_to_movie_titles.items():
    clean_book_title = ada.matching.normalize_title(raw_book_title)
    if clean_book_title not in title_to_book_metas:
        continue

    has_match = False

    for raw_movie_title in raw_movie_titles:
        clean_movie_title = ada.matching.normalize_title(raw_movie_title)
        if clean_movie_title not in title_to_movie_metas:
            continue

        has_match = True
        for movie_meta in title_to_movie_metas[clean_movie_title]:
            movie_asin = movie_meta["asin"]
            asin_to_franchise_id[movie_asin] = franchise_id

    if has_match:
        for book_meta in title_to_book_metas[clean_book_title]:
            book_asin = book_meta["asin"]
            asin_to_franchise_id[book_asin] = franchise_id
        franchise_id += 1


print(f"Number of asin values: {len(asin_to_franchise_id)}")
print(f"Number of frachises: {franchise_id}")



def add_franchise_id(df, asin_to_franchise_id):
    df['franchise_id'] = df['asin'].apply(lambda x: asin_to_franchise_id[x] if x in asin_to_franchise_id else None)

add_franchise_id(books_df, asin_to_franchise_id)
add_franchise_id(movies_df, asin_to_franchise_id)
books_df.to_json(data.get_path("merged_clean_Books", use_gzip=False), orient='records')
movies_df.to_json(data.get_path("merged_clean_Movies", use_gzip=False), orient='records')
