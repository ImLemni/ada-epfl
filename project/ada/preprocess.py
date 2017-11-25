import ada
import os

from ada.ordering import natural_comparator
from ada.stream_tools import chunked_merge_sort


def normalize_json(in_name: str, out_name: str) -> None:
    entries = ada.data.read_data(in_name, None)
    ada.data.write_data(out_name, entries)


def asin_comparator(left, right):
    return natural_comparator(left["asin"], right["asin"])


def sort_by_asin(in_name: str, out_name: str) -> None:
    entries = ada.data.read_data(in_name, None)
    sorted = chunked_merge_sort(entries, asin_comparator)
    ada.data.write_data(out_name, sorted)


def map_meta_review(meta_review):
    """
    TODO: Clean up how we deal with pairs obtained by joining the metadata with the reviews
    :param meta_review:
    :return:
    """
    for meta, review in meta_review:
        yield [meta, review]


def run():
    normalize_dict = {
        "meta_Amazon_Instant_Video": "meta_videos-asin",
        "meta_Movies_and_TV": "meta_movies-asin",
        "meta_Books": "meta_books-asin",
        "reviews_Amazon_Instant_Video": "reviews_videos-asin",
        "reviews_Movies_and_TV": "reviews_movies-asin",
    }

    for in_name, out_name in normalize_dict.items():
        if not os.path.isfile(ada.data.get_path(out_name)):
            print(f"Normalizing and sorting {in_name} to {out_name}")
            sort_by_asin(in_name, out_name)

    if not os.path.isfile(ada.data.get_path("movies")):
        print("Joining movie metadata with reviews")
        meta = ada.data.read_data("meta_movies-asin", None)
        reviews = ada.data.read_data("reviews_movies-asin", None)
        joined = ada.stream_tools.left_join(meta, reviews, "asin")
        ada.data.write_data("movies", map_meta_review(joined))


if __name__ == "__main__":
    run()
