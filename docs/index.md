---
layout: default
---

## Can we finally be sure that Harry Potter is, from far, better as a book ?

### Introduction

Today, many Intellectual Properties are declined into multiple supports. For example, books are turned into movies, series, theater plays, video games; or the other way around. Each platform has its own specificities and their audience may have different expectations. We will focus on books and movies/TV.
This common debate is really animated, who has never heard after watching a movie that : "It was good but I prefered the book" ?

We would like to find out what are the differences and similarities between these supports. Are books better rated than movies? Does the price or the time impact rating ? Can we identify different consumer profiles? We intend to use the Amazon products dataset. The reviews will help us to derive interest for a product. We are also able to find people who gave a review for movies and books of the same franchise aswell are the sentiment of their reviews.


### Summary

* [Initial data](#initial-data)
* [Filtering](#filtering)
* [Sentiment analysis and final data](#sentiment-analysis-and-final-data)
* [First overview](#first-overview)
* [Clustering reviews](#clustering-reviews)
* [Categorizing users](#categorizing-users)
* [Mentions of the book or the movie](#mentions-of-the-book-or-the-movie)
* [Order of the reviews](#order-of-the-reviews)
* [Users buying all the products](#users-buying-all-the-products)
* [More criteria](#more-criteria)
* [Conclusion](#conclusion)


### Initial data

We used the Amazon dataset, especially reviews and metadata for books and Movies_and_TV categories.
On one side we have reviews, containing for example the grade(refered as "overall" in the following), the review content and the user idea,
on the other hand we have the metadata for a product with the title, the price or the description.

#### Books
<b id="counter1"></b>
<b id="counter2"></b>
<b id="counter3"></b>

#### Movies
<b id="counter4"></b>
<b id="counter5"></b>
<b id="counter6"></b>


### Filtering

Now that we have gathered the data, we have to filter it. In order to get meaningful results,
we have chosen to scrap wikipedia to obtain associations between books and movies.
<a href ="https://en.wikipedia.org/wiki/Lists_of_fiction_works_made_into_feature_films"> <img src="images/wikipediatitles.png" alt="wikipedia association"></a>

The complex task is then to associate a title collected via wikipedia with an Amazon product id.
Let's take an example : we want to match the movie `The Three Musketeers` with the product `The Three Musketeers (Golden Films) [VHS]`
<img src="images/filtering.png" alt="wikipedia association">
As it is not necessarily enough, we also take care of accents, punctuation, keywords such as `dvd` or `vhs` or badly encoded characted

We then keep only movies and books for which we could manage to find at least one matching product for both.
#### Books
<b id="counter7"></b>
<b id="counter8"></b>
<b id="counter9"></b>

#### Movies
<b id="counter10"></b>
<b id="counter11"></b>
<b id="counter12"></b>

### Sentiment analysis and final data

Using the [vader](https://github.com/cjhutto/vaderSentiment) package we gave to each text review a value between 0 and 1 (originally between -1 and 1) representing its overall sentiment :
  * Between 0 and 0.25 the review is negative
  * Between 0.25 and 0.75 the review is neutral
  * Abose it is positive
This analysis take into account negations, punctuation (!!!),  word-shape, emoticons acronyms and so on, which are often used in our reviews.

Before ending the data handling part, we also computed a special subset containing only books reviews which can be matched witha review about a paired movie made by the same user (and vice versa). This subset is composed of 2000 users and 3000 paired reviews.

### First overview

TODO : Basic analysis between books and movies

### Clustering reviews

*You might think that when you read a book and see a movie, you always prefer one so you will give a good grade and positive review to one and worse grade and review to the other, but is it always that strict ?*

We have used the Kmeans clustering method to try to answer this question. We have decided to fix the number of categories to 5 and we used the combination of overall grades(`overall`) and sentiment measurement (refered as `compound`) for both movies and books as a metric.

TODO insert picture here

If we look at the meaning of each cluster we obtain something close to this :
* Cluster 0 (in orange): good grades and reviews for movies and books
* Cluster 1 (in yellow): Bad review and bad grade for movies, good review and grade for books
* Cluster 2 (in green): Generally good but negative reviews for books
* Cluster 3 (in red): Bad grade for movies
* Cluster 4 (in black): Bad reviews for both movies and books

### Categorizing users

*But everyone knows that there is always this guy, who always have read the book and always criticize the movie !*

**Do people who give many reviews always belong to the same cluster ?**

TODO : plot and redo analysis

We can see a big majority for cluster 0: people who give good grades and reviews for both movies and books in a review tend to do the same for all franchises. However we can not really say that users always give bad grades for movies (clusters 1 and 3)

### Mentions of the book or the movie

*One thing that is sure, is that if you have read the book and have watched the movie, a bad grade is obviously influenced by the other one*

**Do the worst/better grades and reviews mention the book/movie ?**

TODO plot + analysis

### Order of the reviews

*blablabla*

**Does reading the book before seing the movie has an impact ?**

### Users buying all the products

*Like for Star Wars, there are people buying all products linked to the same movie, they must give really good grades!*

### More criteria

*Ok, you won.. Now just tell me if the book is better than the movie*

Before trying to give an answer to our initial question it remains a few important criteria to analyse.

**Do the grades and reviews changed during time ?**

Since we have data over a pretty long range of time (1996-2014), it is interesting to look at the evolution of grades and reviews. However we lack some contextual information that could help us interpret the results with more confidence.

**Is the cost impactful ?**

**Quality of the product**

One big bias that we had to talk about is the one generated by the quality of the product. With a book for example, with the same text content there are many other criteria that are taken into account in the final grade (quality of the paper,format..).

### Conclusion
