from ada import data
import filterData
import pandas as pd


def build_new_review_df(use_products, file, line_num):
    reviews_lines = data.read_data(file, line_num)
    i = 0
    df = {}
    for line in reviews_lines:
        if line["asin"] in use_products:
            df[i] = line
            i += 1
    return pd.DataFrame.from_dict(df, orient='index')


wiki_dict,books_match, movies_match = filterData.get_matching_product()
# We build a dict as it is implemented as an hash table and we want a complexity
# for checking presence of an element in O(1)

books_product_id = {}
for books in books_match.values():
    for book in books:
        books_product_id[book["asin"]] = book

movies_product_id = {}
for movies in movies_match.values():
    for movie in movies:
        movies_product_id[movie["asin"]] = movie

print(f"We have {len(movies_product_id.keys())} distincts product for movies")
print(f"We have {len(books_product_id.keys())} distincts product for books")

books_new_df = build_new_review_df(books_product_id, "reviews_Books", 22507155)
books_new_df.shape
books_new_df.to_json("filtered_Books_reviews.json", orient='records')

movies_new_df = build_new_review_df(
    movies_product_id, "reviews_Movies_and_TV", 4607047)
movies_new_df.shape
movies_new_df.to_json("filtered_Movies_reviews.json", orient='records')

books_meta_filtered_df = build_new_review_df(
    books_product_id, "meta_Books", 2370585)
books_meta_filtered_df.shape
books_meta_filtered_df.to_json("filtered_Books_meta.json", orient='records')

movies_meta_filetered_df = build_new_review_df(
    movies_product_id, "meta_Movies_and_TV", 208321)
movies_meta_filetered_df.shape
movies_meta_filetered_df.to_json("filtered_Movies_meta.json", orient='records')

books_reviews_f = pd.read_json("filtered_Books_reviews.json", orient='records')
books_meta_f = pd.read_json("filtered_Books_meta.json", orient='records')
books_reviews_f.shape
books_filtered = books_reviews_f.merge(books_meta_f, on="asin")
books_filtered.shape
books_filtered.head(5)
books_filtered.to_json("filtered_merged_Books.json", orient='records')
books_filtered.head(5)

movies_reviews_f = pd.read_json(
    "filtered_Movies_reviews.json", orient='records')
movies_meta_f = pd.read_json("filtered_Movies_meta.json", orient='records')
movies_reviews_f.shape
movies_filtered = movies_reviews_f.merge(movies_meta_f, on="asin")
movies_filtered.shape
movies_filtered.to_json("filtered_merged_Movies.json", orient='records')
movies_filtered.head(5)
