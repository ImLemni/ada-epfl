from ada import data
import filterData
import pandas as pd
from ada.getListOfBooks import get_dict_titles
from filterData import clean_title


def filter_merged_df(df):
    df = df.drop("reviewTime", 1)
    df = df.drop("reviewerName", 1)
    df = df.drop("imUrl", 1)
    df = df.drop("categories", 1)
    df = df.drop("salesRank", 1)
    df['helpful'] = df['helpful'].apply(
        lambda x: x[1] if x[1] == 0 else x[0] / x[1])
    df = df.drop("related", 1)
    return df


def add_franchise_id(df, franchise_dict):
    df['franchise_id']=df['asin'].apply(lambda x: franchise_dict[x])
    return df

wiki_dict, books_match, movies_match = filterData.get_matching_product()


product_to_franchise = {}
franchise_id = 0
for k, v in wiki_dict.items():
    associate = False
    if clean_title(k) in books_match and len(books_match[clean_title(k)]) > 0:
        for mov in v:
            if clean_title(mov) in movies_match and len(movies_match[clean_title(mov)]) > 0:
                associate = True
                for movie_product in movies_match[clean_title(mov)]:
                    product_to_franchise[movie_product['asin']] = franchise_id
        for book_product in books_match[clean_title(k)]:
            product_to_franchise[book_product['asin']] = franchise_id
    franchise_id += 1 if associate else 0


movies_df = pd.read_json("filtered_merged_Movies.json", orient='records')
books_df = pd.read_json("filtered_merged_Books.json", orient='records')

movies_df = filter_merged_df(movies_df)
movies_df = add_franchise_id(movies_df,product_to_franchise)
movies_df.to_json("merged_clean_Movies.json", orient='records')
books_df = filter_merged_df(books_df)
books_df = add_franchise_id(books_df,product_to_franchise)
books_df.to_json("merged_clean_Books.json", orient='records')
