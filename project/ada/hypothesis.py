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


if __name__ == "__main__":
    print("Testing if meta_videos is sorted by `asin`:")
    print(is_sorted_by_asin(read_data("meta_videos", None)))

    print("Testing if meta_movies is sorted by `asin`:")
    print(is_sorted_by_asin(read_data("meta_movies", None)))

    print("Testing if meta_books is sorted by `asin`:")
    print(is_sorted_by_asin(read_data("meta_books", None)))

    print("Testing if meta_movies_asin_sorted is sorted by `asin`:")
    print(is_sorted_by_asin(read_data("meta_movies_asin_sorted", None)))
