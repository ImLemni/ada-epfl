import pandas as pd
from ada import data
import numpy as np
from ada.progressbar import ProgressBar
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sb
from sklearn.cluster import KMeans
from sklearn import linear_model

books_df = pd.read_json(data.get_path(
    "../merged_clean_Books", use_gzip=False), orient="records")
movies_df = pd.read_json(data.get_path(
    "../merged_clean_Movies", use_gzip=False), orient="records")

analyser = SentimentIntensityAnalyzer()
movies_df['sentiment'] = movies_df['reviewText'].apply(
    lambda x: analyser.polarity_scores(x))
books_df['sentiment'] = books_df['reviewText'].apply(
    lambda x: analyser.polarity_scores(x))
books_df.head()


def split_sentiment(x):
    """
    Split a dictionary of sentiment polarity into a serie.
    - `neg`: negative
    - `neu`: neutral
    - `pos`: positive
    - `compound`: compound
    """
    return pd.Series([x['neg'], x['neu'], x['pos'], x['compound']])


movies_df[['neg', 'neu', 'pos', 'compound']
          ] = movies_df['sentiment'].apply(split_sentiment)
books_df[['neg', 'neu', 'pos', 'compound']
         ] = books_df['sentiment'].apply(split_sentiment)

print(len(books_df['asin'].unique()))
print(len(movies_df['asin'].unique()))

movies_users = movies_df['reviewerID'].unique()
books_users = books_df['reviewerID'].unique()
users_both = np.intersect1d(movies_users, books_users)
len(users_both)

user_same_franchise = []
with ProgressBar(len(users_both)) as progress_bar:
    for user in users_both:
        movies_reviews_fr = movies_df[movies_df["reviewerID"]
                                      == user]["franchise_id"].unique()
        books_reviews_fr = books_df[books_df["reviewerID"]
                                    == user]["franchise_id"].unique()
        if len(np.intersect1d(movies_reviews_fr, books_reviews_fr)) > 0:
            user_same_franchise.append({"user": user, "franchises": np.intersect1d(
                movies_reviews_fr, books_reviews_fr)})
        progress_bar.update(1)

len(user_same_franchise)

mov_m = pd.DataFrame()
book_m = pd.DataFrame()
with ProgressBar(len(user_same_franchise)) as progress_bar:
    for user_dict in user_same_franchise:
        for fr in user_dict['franchises']:
            mov_m = mov_m.append(movies_df[(movies_df["reviewerID"] == user_dict['user']) & (
                movies_df["franchise_id"] == fr)])

            book_m = book_m.append(books_df[(books_df["reviewerID"] == user_dict['user']) & (
                books_df["franchise_id"] == fr)])
        progress_bar.update(1)


mov_m.head(5)


def plotCor(df1, df2, y, x, title, suffixa=" for movies", suffixb=" for books"):
    zone, (plot1, plot2) = plt.subplots(ncols=2, sharey=True, sharex=True)
    zone.set_size_inches(16, 6)

    plot1 = sb.regplot(y=y, x=x, data=df1, ax=plot1, x_bins=10)
    plot1.set_title(title + suffixa)

    plot2 = sb.regplot(y=y, x=x, data=df2, ax=plot2, x_bins=10)
    plot2.set_title(title + suffixb)
    plt.show()


merged_df = mov_m.merge(book_m, on=["reviewerID", "franchise_id"],
                        suffixes=["_movies", "_books"])
merged_df = merged_df[['asin_movies', 'asin_books', 'reviewerID', 'franchise_id', "overall_movies",  "neg_movies", "neu_movies",
                       "pos_movies", "compound_movies", "overall_books", "neg_books", "neu_books", "pos_books", "compound_books", "unixReviewTime_books", "unixReviewTime_movies"]]
merged_df.head()


def normalizeColumn(df, columns):
    for column in columns:
        df[column] = (df[column] - df[column].min()) / \
            (df[column].max() - df[column].min())
    return df


merged_df = normalizeColumn(
    merged_df, ["overall_movies", "overall_books", "compound_movies", "compound_books"])

merged_df_fil = merged_df[["overall_movies",
                           "overall_books", "compound_movies", "compound_books"]]

npdf = merged_df_fil.values

kmeans = KMeans(n_clusters=5, random_state=100).fit(npdf)
print(kmeans.cluster_centers_)
# Cluster 0 : good grades and reviews for movies and books
# Cluster 1 : Bad review and bad grade for movies, good review and grade for books
# Cluster 2 : Negative review foor book but positive review for movies
# Cluster 3 : Bad grade for movies
# Cluster 4 : Bad reviews for both movies and books
kmeans_df = pd.DataFrame(np.c_[npdf, kmeans.labels_, merged_df["reviewerID"].values], columns=[
    "overall_movies", "overall_books", "compound_movies", "compound_books", "cluster", "reviewerID"])
color_dict = {0.0: "#fc8d59", 1.0: "#ffffbf",
              2.0: "#91cf60", 3.0: "#ff2727", 4.0: "#000000"}
kmeans_df["color"] = kmeans_df["cluster"].map(color_dict)
kmeans_df.head()

# sb.regplot(data=kmeans_df, x="overall_movies", y="overall_books",
#             scatter_kws={'c': kmeans_df['color']})
# plt.show()
scatterplot = kmeans_df.plot.scatter(
    x="overall_movies", y="overall_books", figsize=(10, 10), c=kmeans_df['color'], s=200)
plt.show()
scatterplot = kmeans_df.plot.scatter(
    x="compound_movies", y="compound_books", figsize=(10, 10), c=kmeans_df['color'], s=200)
plt.show()
scatterplot = kmeans_df.plot.scatter(
    x="overall_books", y="compound_books", figsize=(10, 10), c=kmeans_df['color'], s=200)
plt.show()
scatterplot = kmeans_df.plot.scatter(
    x="overall_movies", y="compound_movies", figsize=(10, 10), c=kmeans_df['color'], s=200)
plt.show()

threedee = plt.figure().gca(projection='3d')
threedee.scatter(kmeans_df["overall_books"],
                 kmeans_df["compound_books"], kmeans_df["overall_movies"], c=kmeans_df['color'])
threedee.set_xlabel('Overall score for books')
threedee.set_ylabel('Sentiment for books')
threedee.set_zlabel('Overall score for movies')
plt.show()

# Does people who gave many reviews always belong to the same cluster
kmeans_df[kmeans_df.duplicated(subset=[
    "overall_movies", "overall_books", "compound_movies", "compound_books"], keep=False)]
# Note that we have some duplicates, when looking at the reviews and products it is
# just that often a same user copy paste its review for 2 distinct products

multi_rating = kmeans_df[kmeans_df.duplicated(
    subset=["reviewerID"], keep=False)]
# 38% of reviews are made by people who gave more than one review
multi_rating.shape[0] / kmeans_df.shape[0]
multi_rating_gb = pd.DataFrame()
multi_rating_gb["unique"] = multi_rating.groupby(["reviewerID"])[
    "cluster"].nunique()
multi_rating_gb["total"] = multi_rating.groupby(["reviewerID"])[
    "cluster"].count()
multi_rating_gb = multi_rating_gb.reset_index()
multi_rating_gb.plot.scatter(
    x="total", y="unique", figsize=(10, 10))
plt.show()

list_user_unique_cluster = multi_rating_gb[multi_rating_gb["unique"] == 1]["reviewerID"].tolist(
)
multi_rating[multi_rating["reviewerID"].isin(
    list_user_unique_cluster)].groupby(["cluster"])["reviewerID"].nunique().plot(kind="bar")
plt.show()
# We can see a big majority for cluster 0:
# People who give good grades and reviews for both movies and books in a review
# tends to do the same for all franchises


clf = linear_model.SGDRegressor()
clf.fit(merged_df_fil[["overall_books", "compound_books"]],
        merged_df_fil["overall_movies"])
clf.score(merged_df_fil[["overall_books", "compound_books"]],
          merged_df_fil["overall_movies"])
# Conclusion : we do not have engouh features to make a good regression (and maybe it's not linear)


mov_m_with_b = mov_m[mov_m["reviewText"].str.contains("book|read")]
mov_m_with_b.shape[0] / mov_m.shape[0]
book_m_with_b = book_m[book_m["reviewText"].str.contains("film|movie")]
book_m_with_b.shape[0] / book_m.shape[0]
# We have tried more complex combination but it is not realy accurate, for example if we add the word "see" for the books we add
# many reviews but by looking at them we can see that it is not really relevant
mov_m_with_b.describe()
book_m_with_b.describe()
plotCor(mov_m_with_b, mov_m, y="neg", x="overall", title="Negativity function of score",
        suffixa=" for reviews speaking of the book", suffixb=" for any review")
plotCor(mov_m_with_b, mov_m, y="pos", x="overall", title="Positivity function of score",
        suffixa=" for reviews speaking of the book", suffixb=" for any review")

plotCor(book_m_with_b, book_m, y="neg", x="overall", title="Negativity function of score ",
        suffixa=" for reviews speaking of the movie", suffixb=" for any review")
plotCor(book_m_with_b, book_m, y="pos", x="overall", title="Positivity function of score",
        suffixa=" for reviews speaking of the movie", suffixb=" for any review")


# Let"s also see which percentage contains those reference for each grade
mov_m["reference_book"] = mov_m["reviewText"].str.contains(
    "book|read").astype(int)
mov_m.head()
book_m["reference_movie"] = book_m["reviewText"].str.contains(
    "film|movie").astype(int)
mov_m_gb_ref = mov_m.groupby(['overall']).agg({'reference_book': 'sum'})[
    "reference_book"] / mov_m.groupby(['overall']).agg({'reference_book': 'count'})["reference_book"]
mov_m_gb_ref.plot(kind='bar')
plt.show()
book_m_gb_ref = book_m.groupby(['overall']).agg({'reference_movie': 'sum'})[
    "reference_movie"] / book_m.groupby(['overall']).agg({'reference_movie': 'count'})["reference_movie"]
book_m_gb_ref.plot(kind='bar')
plt.show()
cutSpace = np.linspace(-1, 1, 21)
mov_m_sent_ref = mov_m.groupby(pd.cut(mov_m["compound"], cutSpace)).agg({'reference_book': 'sum'})[
    "reference_book"] / mov_m.groupby(pd.cut(mov_m["compound"], cutSpace)).agg({'reference_book': 'count'})["reference_book"]
book_m_sent_ref = book_m.groupby(pd.cut(book_m["compound"], cutSpace)).agg({'reference_movie': 'sum'})[
    "reference_movie"] / book_m.groupby(pd.cut(book_m["compound"], cutSpace)).agg({'reference_movie': 'count'})["reference_movie"]
mov_m_sent_ref.plot(kind="bar")
plt.show()
book_m_sent_ref.plot(kind="bar")
plt.show()


# Impact of the time
books_bf_movies = merged_df[merged_df["unixReviewTime_books"]
                            < merged_df["unixReviewTime_movies"]]
books_at_movies = merged_df[merged_df["unixReviewTime_books"]
                            > merged_df["unixReviewTime_movies"]]
books_se_movies = merged_df[merged_df["unixReviewTime_books"]
                            == merged_df["unixReviewTime_movies"]]

print(f"Review for book before review for movie : {100 * books_bf_movies.shape[0]/merged_df.shape[0]} %")
print(f"Review for movie before review for book : {100 * books_at_movies.shape[0]/merged_df.shape[0]} %")
print(f"Reviews the same day : {100 * books_se_movies.shape[0]/merged_df.shape[0]} %")
result_time_df = pd.DataFrame(columns=["Context", "Mean books", "Mean movies", "Mean compound_books",
                                       "Mean compound_movies", "std books", "std_movies", "std comp books", "std comp movies"])
result_time_df.loc[0] = ["Book before movie", books_bf_movies["overall_books"].mean(), books_bf_movies["overall_movies"].mean(), books_bf_movies["compound_books"].mean(), books_bf_movies["compound_movies"].mean(),
                         books_bf_movies["overall_books"].std(), books_bf_movies["overall_movies"].std(), books_bf_movies["compound_books"].std(), books_bf_movies["compound_movies"].std()]
result_time_df.loc[1] = ["Book before movie", books_at_movies["overall_books"].mean(), books_at_movies["overall_movies"].mean(), books_at_movies["compound_books"].mean(), books_at_movies["compound_movies"].mean(),
                         books_at_movies["overall_books"].std(), books_at_movies["overall_movies"].std(), books_at_movies["compound_books"].std(), books_at_movies["compound_movies"].std()]
result_time_df.loc[2] = ["Book before movie", books_se_movies["overall_books"].mean(), books_se_movies["overall_movies"].mean(), books_se_movies["compound_books"].mean(), books_se_movies["compound_movies"].mean(),
                         books_se_movies["overall_books"].std(), books_se_movies["overall_movies"].std(), books_se_movies["compound_books"].std(), books_se_movies["compound_movies"].std()]
result_time_df

zone, (plot1, plot2, plot3) = plt.subplots(ncols=3)
zone.set_size_inches(16, 8)

plot1 = sb.boxplot(y='overall_books', data=books_bf_movies, ax=plot1)
plot1.set_title("Overall grades for books(book before movie)")

plot2 = sb.boxplot(y='overall_books', data=books_at_movies, ax=plot2)
plot2.set_title("Overall grades for books(book after movie)")

plot3 = sb.boxplot(y='overall_books', data=books_se_movies, ax=plot3)
plot3.set_title("Overall grades for books(book same movie)")
plt.show()

# Let's try to see if there is a difference per grade
(books_bf_movies.groupby([books_bf_movies["overall_books"]])[
 "overall_books"].count() / books_bf_movies.shape[0]).plot(kind='bar')
plt.show()
(books_at_movies.groupby([books_at_movies["overall_books"]])[
 "overall_books"].count() / books_at_movies.shape[0]).plot(kind='bar')
plt.show()
(books_se_movies.groupby([books_se_movies["overall_books"]])[
 "overall_books"].count() / books_se_movies.shape[0]).plot(kind='bar')
plt.show()

# merged_df[(merged_df["overall_books"] == 1) & (
#     merged_df["unixReviewTime_books"] < merged_df["unixReviewTime_movies"])]["overall_books"].count()
# merged_df[(merged_df["overall_books"] == 1) & (
#     merged_df["unixReviewTime_books"] > merged_df["unixReviewTime_movies"])]["overall_books"].count()
# merged_df[(merged_df["overall_books"] == 1) & (
#     merged_df["unixReviewTime_books"] == merged_df["unixReviewTime_movies"])]["overall_books"].count()
# merged_df[merged_df["overall_books"] == 1]["overall_books"].count()


def plot_impact_time(groupby, main_col):
    time_impact_df_bf = merged_df.groupby(groupby)[["unixReviewTime_movies", "unixReviewTime_books"]].apply(
        lambda x: x[x["unixReviewTime_movies"] > x["unixReviewTime_books"]].count() / x.shape[0])
    time_impact_df_bf = time_impact_df_bf.reset_index().drop(
        time_impact_df_bf.columns[len(time_impact_df_bf.columns) - 1], axis=1)
    time_impact_df_bf.columns = [main_col, "book before movie"]

    time_impact_df_at = merged_df.groupby(groupby)[["unixReviewTime_movies", "unixReviewTime_books"]].apply(
        lambda x: x[x["unixReviewTime_movies"] < x["unixReviewTime_books"]].count() / x.shape[0])
    time_impact_df_at = time_impact_df_at.reset_index().drop(
        time_impact_df_at.columns[len(time_impact_df_at.columns) - 1], axis=1)
    time_impact_df_at.columns = [main_col, "book after movie"]

    time_impact_df_se = merged_df.groupby(groupby)[["unixReviewTime_movies", "unixReviewTime_books"]].apply(
        lambda x: x[x["unixReviewTime_movies"] == x["unixReviewTime_books"]].count() / x.shape[0])
    time_impact_df_se = time_impact_df_se.reset_index().drop(
        time_impact_df_se.columns[len(time_impact_df_se.columns) - 1], axis=1)
    time_impact_df_se.columns = [main_col, "book same day movie"]

    time_impact_df = time_impact_df_bf.merge(
        time_impact_df_at).merge(time_impact_df_se)
    time_impact_df.plot(kind="bar", x=main_col)
    plt.show()


plot_impact_time("overall_books", "overall_books")
plot_impact_time("overall_movies", "overall_movies")
plot_impact_time(
    pd.cut(merged_df["compound_books"], np.linspace(-1, 1, 6)), "compound_books")
plot_impact_time(
    pd.cut(merged_df["compound_movies"], np.linspace(-1, 1, 6)), "compound_movies")


# Time for grades/reviews for movies
movies_df.groupby(pd.cut(movies_df["unixReviewTime"], 10))["overall"].mean()
movies_df.groupby(pd.cut(movies_df["unixReviewTime"], 10))["overall"].std()
movies_df["dateTime"] = pd.to_datetime(
    movies_df["unixReviewTime"], unit="s", origin='unix')
movies_df.head()
errors = movies_df.resample('M', on="dateTime").std()
errors_overall = errors["overall"]
movies_df.resample('M', on="dateTime").mean().plot(
    y="overall", yerr=errors_overall)
plt.show()
errors_compound = errors["compound"]
movies_df.resample('M', on="dateTime").mean().plot(
    y="compound", yerr=errors_compound)
plt.show()

# Time for grades/reviews for books
books_df["dateTime"] = pd.to_datetime(
    books_df["unixReviewTime"], unit="s", origin='unix')
b_errors = books_df.resample('M', on="dateTime").std()
b_errors_overall = b_errors["overall"]
books_df.resample('M', on="dateTime").mean().plot(
    y="overall", yerr=b_errors_overall)
plt.show()
b_errors_compound = b_errors["compound"]
books_df.resample('M', on="dateTime").mean().plot(
    y="compound", yerr=errors_compound)
plt.show()

# Compute each product release date (=first review)
release_date_books = books_df.groupby(["asin"])["unixReviewTime"].min()
release_date_movies = movies_df.groupby(["asin"])["unixReviewTime"].min()
# Impact of release date

# People buying all or a majority of products linked to the same franchise_id
# Doing it only for people buying both movies and books products as other
# case is not releavant for our study
unique_per_fr = merged_df.groupby(["franchise_id"])[
    ["asin_books", "asin_movies"]].nunique()
unique_per_fr[unique_per_fr["asin_books"] + unique_per_fr["asin_movies"] > 2]
unique_per_user_per_fr = merged_df.groupby(["reviewerID", "franchise_id"])[
    ["asin_books", "asin_movies"]].nunique()
unique_per_user_per_fr[unique_per_user_per_fr["asin_books"] +
                       unique_per_user_per_fr["asin_movies"] > 2]
result_list_unique_fr = []
for fr_id in unique_per_fr.index:
    th = unique_per_fr.loc[fr_id]["asin_books"] + \
        unique_per_fr.loc[fr_id]["asin_movies"]

    temp = unique_per_user_per_fr.xs(fr_id, level='franchise_id')
    result_list_unique_fr += temp[(temp["asin_books"] +
                                   temp["asin_movies"]) > max(0.5 * th, 2)].index.tolist()


#  44 occurences of buying more than 50% of the franchise products
len(result_list_unique_fr)
len(set(result_list_unique_fr))

buy_everything_df = merged_df[merged_df["reviewerID"].isin(
    result_list_unique_fr)]
buy_everything_df.describe()
buy_everything_df[["overall_movies", "overall_books", "compound_movies", "compound_books"]].mean().plot.bar(
    yerr=buy_everything_df[["overall_movies", "overall_books", "compound_movies", "compound_books"]].std())
plt.show()
merged_df[["overall_movies", "overall_books", "compound_movies", "compound_books"]].mean().plot.bar(
    yerr=merged_df[["overall_movies", "overall_books", "compound_movies", "compound_books"]].std())
plt.show()


def same_plot_bar(dflist, namelist, xlegend):
    pos = list(range(len(dflist[0].mean())))
    width = 1.0 / (1 + len(dflist))
    fig, ax = plt.subplots(figsize=(16, 8))
    for numb, df in enumerate(dflist):
        plt.bar([p + numb * width for p in pos],
                df.mean(),
                width,
                color='C' + str(numb),
                yerr=df.std())

    ax.set_xticks([p + len(dflist) * 0.25 * width for p in pos])
    ax.set_xticklabels(xlegend)
    plt.legend(namelist, loc='upper left')
    plt.axhline(0, color='black')
    plt.show()


same_plot_bar([buy_everything_df[["overall_movies", "overall_books", "compound_movies", "compound_books"]], merged_df[[
              "overall_movies", "overall_books", "compound_movies", "compound_books"]]], ["Buy most", "All"], ["overall_movies", "overall_books", "compound_movies", "compound_books"])

# Impact of the price over all reviews/grades
plotCor(movies_df, books_df, "overall", "price",
        "Relation overall = f(price)")  # already done in milestone2
plotCor(movies_df, books_df, "compound", "price",
        "Relation compound = f(price)")
same_plot_bar([movies_df.groupby(pd.cut(movies_df["price"], np.linspace(0, 40, 11)))["overall"], books_df.groupby(
    pd.cut(books_df["price"], np.linspace(0, 40, 11)))["overall"]], ["movie grade", "book grade"], np.linspace(0, 40, 11))
same_plot_bar([movies_df.groupby(pd.cut(movies_df["price"], np.linspace(0, 40, 11)))["compound"], books_df.groupby(
    pd.cut(books_df["price"], np.linspace(0, 40, 11)))["compound"]], ["movie compound", "book compound"], np.linspace(0, 40, 11))
# Impact of the price for people who already buy other product of the franchise
plotCor(mov_m, book_m, "overall", "price",
        "Relation overall = f(price)")  # already done in milestone2
plotCor(mov_m, book_m, "compound", "price",
        "Relation compound = f(price)")
same_plot_bar([mov_m.groupby(pd.cut(mov_m["price"], np.linspace(0, 40, 11)))["overall"], book_m.groupby(
    pd.cut(book_m["price"], np.linspace(0, 40, 11)))["overall"]], ["movie grade", "book grade"], np.linspace(0, 40, 11))
same_plot_bar([mov_m.groupby(pd.cut(mov_m["price"], np.linspace(0, 40, 11)))["compound"], book_m.groupby(
    pd.cut(book_m["price"], np.linspace(0, 40, 11)))["compound"]], ["movie compound", "book compound"], np.linspace(0, 40, 11))


same_plot_bar([mov_m.groupby(pd.cut(mov_m["price"], np.linspace(0, 40, 11)))["overall"], movies_df.groupby(
    pd.cut(movies_df["price"], np.linspace(0, 40, 11)))["overall"]], ["movie grade filtered", "movie grade all"], np.linspace(0, 40, 11))
same_plot_bar([mov_m.groupby(pd.cut(mov_m["price"], np.linspace(0, 40, 11)))["compound"], movies_df.groupby(
    pd.cut(movies_df["price"], np.linspace(0, 40, 11)))["compound"]], ["movie compound filtered", "movie compound all"], np.linspace(0, 40, 11))

same_plot_bar([book_m.groupby(pd.cut(book_m["price"], np.linspace(0, 40, 11)))["overall"], books_df.groupby(
    pd.cut(books_df["price"], np.linspace(0, 40, 11)))["overall"]], ["book grade filtered", "book grade all"], np.linspace(0, 40, 11))
same_plot_bar([book_m.groupby(pd.cut(book_m["price"], np.linspace(0, 40, 11)))["compound"], books_df.groupby(
    pd.cut(books_df["price"], np.linspace(0, 40, 11)))["compound"]], ["book compound filtered", "book compound all"], np.linspace(0, 40, 11))

# Impact of the product itself when there are more than one product for the same franchise
groupby_fr_asin = movies_df.groupby(["franchise_id", "asin"])[
    "overall", "compound"]
same_plot_bar([groupby_fr_asin.mean(), groupby_fr_asin.median(),
               groupby_fr_asin.min(), groupby_fr_asin.max()], ["Mean", "Median", "Min", "Max"], ["overall", "compound"])
groupby_fr_asin_b = books_df.groupby(["franchise_id", "asin"])[
    "overall", "compound"]
same_plot_bar([groupby_fr_asin_b.mean(), groupby_fr_asin_b.median(),
               groupby_fr_asin_b.min(), groupby_fr_asin_b.max()], ["Mean", "Median", "Min", "Max"], ["overall", "compound"])
