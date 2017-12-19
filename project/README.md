# Is the book better than the movie?

## Abstract

Today, many Intellectual Properties (IP) are declined into multiple supports. For example, books are turned
into movies, series, theater plays, video games; or the other way around. Each platform has its own
specificities and their audience may have different expectations. We will focus on books and movies/TV.
We would like to find out what are the differences and similarities between these supports. Are books
better rated than movies? Was there some evolution during the last 20 years? Can we find some
consumer profiles?
We intend to use the Amazon products dataset. The reviews will help us to derive interest for a product.
We are also able to study the link between the products bought by the same customer. This would allow
us to create a network of products and customers.
Finally, we expect to study time patterns and interactions between the releases on different platforms
and customer behavior (we expect movie releases to boost book releases but there may be more
interesting patterns).

## Research questions

- Are the reviews better for movie or the book?
  - We will have to define more criteria and context to give a concrete answer to this question
- What are the factors of success for each platform (ex. genre, ...)?
  - This question hardly depends on the additional information fetching through the API,
   as we do not have enough data to give a proper answer for now.
- Can we distinguish populations that prefer a certain form of medium?
  - We will answer this question via the analysis of users who gave reviews to both members of
  a pair book/movie.
  - This is also the occasion to build a clustering method that we may expand with a predictive role
- Are there people buying all the products for a license?
  - We have reduced this question with products meaning all the books and movies product linked to the same
   pair book/movies. We did not studied yet the feasibility of expanding this relation to series of books or
   movies.
- Can we find interesting patterns when a release occurs on one platform?
  - We do not know yet if we have enough (both in quantity and quality) data to answer this question.
   We will, at least partially, answer it during the impact of the time in grading.
- Can we find people buying the book after the release of a movie?
  - Same analysis
- Do the bad/good movie reviews mention the book?
  - We will try to mix the use of sentiment analysis, overall grading and keywords in the review text to
  answer this question.

## Dataset

We will use the [Amazon Product Data][amazon-data] dataset.
We will mainly use the "Books" and "Movies & TV" subsets.

We also use [Wikipedia][wikipedia-titles] in order to have a list of matching books/movies titles.
We might use the Amazon product API to obtain additionnal information about products (such as genre..)

## Next steps until Milestone 3

- Improve matching between products and franchise :
  - Improve matching using Wikipedia titles, for example by using text distance
  - Consider other options, such as other sources or matching between Amazon products using title, description and so on.


- Make a more in depth analysis of existing differences between movies and books for a same franchise (overall,sentiment in the reviews..)

- Complete our analysis of the gap between grades made by the same user in the same IP : take the sentiment into account, the influence of the order of reviews in time..

- Study the impact of other features such as the price of the product or the review date


## Usage

You need the `vaderSentiment` package:
```bash
$ source activate
$ pip install vaderSentiment
```

You can configure the data directory by starting the notebook with the `ADA_DATA_PATH` environment
variable. By default, it uses the `data` subdirectory.

This is the directory where data is stored.

```bash
$ source activate
$ ADA_DATA_PATH="/path/to/data" jupyter notebook
```

You can execute the file `Milestone2` to generate all the datafiles and plots.
Most of helper functions are in the modules of the `ada` package (in this directory).


TODO: Mention that we changed the matching function

[amazon-data]: http://jmcauley.ucsd.edu/data/amazon/
[wikipedia-titles]: https://en.wikipedia.org/wiki/Lists_of_fiction_works_made_into_feature_films
