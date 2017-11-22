import pandas as pd
import gzip
import os
from tqdm import tqdm
from getListOfBooks import get_dict_titles
DATAPATH = "/media/lemni/HDD Flo/ADA"


def parse(path, maxInputs):
    with gzip.open(path, 'rb') as g:
        with tqdm(total=maxInputs) as pbar:
            for l in g:
                yield eval(l)
                pbar.update(1)


def getDF(path, maxInputs=0):
    i = 0
    df = {}
    for d in parse(path, maxInputs):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


# For progressbar :
# Books : 22,507,155 reviews 2,370,585 products
# Movies : 4,607,047 reviews 208,321 products
# Amazon instant videos : 583,933 reviews 30,648 products
# df_reviews = getDF(os.path.join(DATAPATH,
#                                 'reviews_Amazon_Instant_Video.json.gz'),
#                                  583933)
# df_meta = getDF(os.path.join(DATAPATH, 'meta_Amazon_Instant_Video.json.gz'),
#                 30648)
# df_merged = df_reviews.merge(df_meta, left_on='asin', right_on='asin',
#                              how='left', copy=False)
df_reviews = getDF(os.path.join(DATAPATH,
                                'reviews_Movies_and_TV.json.gz'), 4607047)
df_meta = getDF(os.path.join(DATAPATH, 'meta_Movies_and_TV.json.gz'), 208321)
df_merged = df_reviews.merge(df_meta, left_on='asin', right_on='asin',
                             how='left', copy=False)
dict_titles = get_dict_titles("https://en.wikipedia.org/wiki/List_of_fiction\
            _works_made_into_feature_films_(D%E2%80%93J)")
pattern = '|'.join(dict_titles.values()).lower()
df_filtered = df_merged[df_merged["title"].str.lower().str.contains(pattern,na=False)]
# TODO replace the previous line with a text distance
print(df_filtered)
