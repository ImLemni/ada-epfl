from datetime import datetime


def describe_reviews(reviews):
    """
    Get a rough description of the provided reviews by iterating over them only once.

    :param reviews: The reviews to describe
    :return: Reviews description: see the returned dictionary below
    """

    size = 0
    unique_asin = set()
    unique_reviewer = set()
    min_unix_time = float("+inf")
    max_unix_time = float("-inf")
    non_rated_comments = 0
    rated_comments = 0
    rating_ratios_sum = 0
    overall_sum = 0

    for review in reviews:
        size += 1
        unique_asin.add(review["asin"])
        unique_reviewer.add(review["reviewerID"])
        overall_sum += review["overall"]

        rated_helpful_count, total_ratings = review["helpful"]
        if total_ratings == 0:
            non_rated_comments += 1
        else:
            rated_comments += 1
            rating_ratios_sum += rated_helpful_count / total_ratings

        min_unix_time = min(min_unix_time, review["unixReviewTime"])
        max_unix_time = max(max_unix_time, review["unixReviewTime"])

    return {
        "size": size,
        "unique_asin": unique_asin,
        "unique_reviewer": unique_reviewer,
        "min_unix_time": min_unix_time,
        "max_unix_time": max_unix_time,
        "non_rated_comments": non_rated_comments,
        "rated_comments": rated_comments,
        "rating_ratios_sum": rating_ratios_sum,
        "overall_sum": overall_sum,
        "reviewer_count": len(unique_reviewer),
        "asin_count": len(unique_asin),
        "unique_reviewer_ratio": len(unique_reviewer) / size if size != 0 else float('nan'),
        "unique_asin_ratio": len(unique_asin) / size if size != 0 else float('nan'),
        "reviews_per_product": size / len(unique_reviewer) if len(unique_reviewer) != 0 else float('nan'),
        "reviews_per_user": size / len(unique_asin) if len(unique_asin) != 0 else float('nan'),
        "average_helpfulness": rating_ratios_sum / rated_comments if rated_comments != 0 else float('nan'),
        "mean_overall": overall_sum / size if size != 0 else float('nan'),
    }


def print_reviews_description(description):
    print(f"""
    Number of unique reviewers: {description['reviewer_count']} ({100*description['unique_reviewer_ratio']}%), {description['reviews_per_user']} reviews per user
    Number of unique products: {description['asin_count']} ({100*description['unique_asin_ratio']}%), {description['reviews_per_product']} reviews per product
    Rated comments (helpfulness): {description['rated_comments']} ({100*description['rated_comments']/description['size']}%)
    Non rated comments (helpfulness): {description['non_rated_comments']} ({100*description['non_rated_comments']/description['size']}%)
    Average comment helpfulness: {description['average_helpfulness']}
    Mean overall score: {description['mean_overall']}
    Time of oldest review: {datetime.fromtimestamp(description['min_unix_time'])} ({description['min_unix_time']})
    Time of newest review: {datetime.fromtimestamp(description['max_unix_time'])} ({description['max_unix_time']})
    """)


def describe_meta(entries, sales_category):
    """
    Get a rough description of the provided metadata by iterating over them only once.

    :param entries: The metadata to describe
    :param sales_category: Main sales category
    :return: Metadata description: see the returned dictionary below
    """

    size = 0
    unique_categories = set()
    sales_rank_min = float("+inf")
    sales_rank_max = float("-inf")
    sales_rank_sum = 0
    sales_rank_count = 0
    title_count = 0
    description_count = 0
    price_count = 0
    price_sum = 0
    related_count = 0

    for entry in entries:
        size += 1
        for category in [category for group in entry["categories"] for category in group]:
            unique_categories.add(category)

        if "salesRank" in entry and sales_category in entry["salesRank"]:
            sales_rank_count += 1
            rank = entry["salesRank"][sales_category]
            sales_rank_sum += rank
            sales_rank_min = min(sales_rank_min, rank)
            sales_rank_max = max(sales_rank_max, rank)

        if "title" in entry:
            title_count += 1

        if "description" in entry:
            description_count += 1

        if "related" in entry:
            related_count += 1

        if "price" in entry:
            price_count += 1
            price_sum += entry["price"]

    return {
        "size": size,
        # "unique_categories": unique_categories,
        "sales_rank_min": sales_rank_min,
        "sales_rank_max": sales_rank_max,
        "sales_rank_sum": sales_rank_sum,
        "sales_rank_count": sales_rank_count,
        "title_count": title_count,
        "description_count": description_count,
        "price_count": price_count,
        "price_sum": price_sum,
        "related_count": related_count,
        "category_count": len(unique_categories),
        "mean_price": price_sum / price_count if price_count != 0 else float('nan'),
        "mean_sales_rank": sales_rank_sum / sales_rank_count if sales_rank_count != 0 else float('nan'),
    }


def print_meta_description(description):
    print(f"""
    Number of products: {description['size']}
    Number of unique categories: {description['category_count']}
    Number of products with price: {description['price_count']} ({100*description['price_count']/description['size']}%)
    Mean price: {description['mean_price']}
    Number of products with sales rank: {description['sales_rank_count']} ({100*description['sales_rank_count']/description['size']}%)
    Mean sales rank: {description['mean_sales_rank']}
    Min sales rank: {description['sales_rank_min']}
    Max sales rank: {description['sales_rank_max']}
    Number of products with a title: {description['title_count']} ({100*description['title_count']/description['size']}%)
    Number of products with a description: {description['description_count']} ({100*description['description_count']/description['size']}%)
    Number of products with a `related` field: {description['related_count']} ({100*description['related_count']/description['size']}%)
    """)
