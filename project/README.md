# Is the book better than the movie?

# Abstract

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

# Research questions

- Are the reviews better for movie or the book?
- What are the factors of success for each platform (ex. genre, ...)?
- Can we distinguish populations that prefer a certain form of medium?
- Are there people buying all the products for a license?
- Can we find interesting patterns when a release occurs on one platform?
- Can we find people buying the book after the release of a movie?
- Do the bad/good movie reviews mention the book?

# Dataset

We will use the [Amazon Product Data][amazon-data] dataset.
We will mainly use the "Books" and "Movies & TV" subsets.

We may also use other sources to help us with matching the books and movies (Wikipedia?).

# A list of internal milestones up until project milestone 2

- Setup a basic environment able to load the data and manipulate it (from the API? from the cluster? should we use a DB?)
- Basic data description: plot distribution, check for missing values
- Devise an algorithm to match different products related to the same Intellectual Property (IP)
- Fetch additional product details
- Perform preliminary analysis on a subset of known IPs and on a given period of time.

# Questions for TAs

- Are we allowed to use the Amazon API to find missing product descriptions?
- What do you prefer? Movies? Books?


[amazon-data]: http://jmcauley.ucsd.edu/data/amazon/
