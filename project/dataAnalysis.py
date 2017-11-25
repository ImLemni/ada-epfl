from ada import data


def get_stats_results(file, line_num):
    reviews_lines = data.read_data(file, line_num)
    distinct_reviewers = set()
    distinct_asin = set()
    totalHelpful = 0
    helpfulCount = 0
    helpfulZero = 0
    overallTotal = 0
    overallCount = 0
    minTime = 2000000000
    maxTime = 0
    for line in reviews_lines:
        distinct_reviewers.add(line["reviewerID"])
        distinct_asin.add(line["asin"])
        helpful = line["helpful"]
        if helpful[0] == 0 and helpful[1] == 0:
            helpfulZero += 1
        else:
            totalHelpful += helpful[0] / helpful[1]
            helpfulCount += 1

        overallTotal += line["overall"]
        unixTime = line["unixReviewTime"]
        maxTime = unixTime if unixTime > maxTime else maxTime
        minTime = unixTime if unixTime < minTime else minTime

    return (distinct_reviewers, distinct_asin, totalHelpful, helpfulCount, helpfulZero, overallTotal, overallCount, minTime, maxTime)


print(get_stats_results("reviews_Books", 6))

books_meta_lines = data.read_data("meta_Books", 2370585)
distinct_categories = set()
sales_rank_min = 100000000
sales_rank_max = 0
sales_rank_total = 0
sales_rank_count = 0
title_count = 0
description_count = 0
price_count = 0
price_total = 0
related_count = 0
for book_line in books_meta_lines:
    for c in book_line["categories"]:
        for v in c:
            distinct_categories.add(v)
    if "salesRank" in book_line and "Books" in book_line["salesRank"]:
        sales_rank_count += 1
        s_rank = book_line["salesRank"]["Books"]
        sales_rank_total += s_rank
        sales_rank_max = s_rank if s_rank > sales_rank_max else sales_rank_max
        sales_rank_min = s_rank if s_rank < sales_rank_min else sales_rank_min
    title_count += 1 if "title" in book_line else 0
    description_count += 1 if "description" in book_line else 0
    if "price" in book_line:
        price_count += 1
        price_total += book_line["price"]
    related_count += 1 if "related" in book_line else 0

sales_rank_min
sales_rank_max
sales_rank_count
100 * sales_rank_count / 2370585
sales_rank_total / sales_rank_count
title_count
description_count
price_count
price_total / price_count
100 * price_count / 2370585
100 * title_count / 2370585
description_count
100 * description_count / 2370585
related_count
100 * related_count / 2370585
