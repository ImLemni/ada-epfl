from ada.data import read_data


def is_sorted_by_asin(entries):
    first = True
    prev = None
    for i, entry in enumerate(entries):
        if first:
            prev = entry
            first = False
            continue
        if prev["asin"] > entry["asin"]:
            print("Not sorted:")
            print(f"Index {i - 1}: {prev}")
            print(f"Index {i}: {entry}")
            return False
    return True


def is_sorted_asin_unique(entries):
    first = True
    prev = None
    for i, entry in enumerate(entries):
        if first:
            prev = entry
            first = False
            continue
        if prev["asin"] == entry["asin"]:
            print("Non unique:")
            print(f"Index {i - 1}: {prev}")
            print(f"Index {i}: {entry}")
            return False
    return True


if __name__ == "__main__":
    check_sorted = [
        "meta_videos",
        "meta_movies",
        "meta_books",
        "meta_videos-asin",
        "meta_movies-asin",
        "meta_books-asin",
    ]

    for in_name in check_sorted:
        print(f"Testing if {in_name} is sorted by `asin`:")
        print(is_sorted_by_asin(read_data(in_name, None)))

    check_unique_asin = [
        "meta_videos-asin",
        "meta_movies-asin",
        "meta_books-asin",
    ]

    for in_name in check_unique_asin:
        print(f"Testing if {in_name} has unique `asin`:")
        print(is_sorted_asin_unique(read_data(in_name, None)))
