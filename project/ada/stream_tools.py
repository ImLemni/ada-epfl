from ada.data import write_data, read_data
from ada.ordering import default_comparator


def next_or_none(iterator):
    """
    Returns the next value of the iterator, or `None` if it reached the end.
    This allows an easier way to consume the iterator than using `try/catch`
    blocks if the iterated collection does not contain any `None` values.

    :param iterator: Iterator to consume. It should not yield `None` values.
    :return: The next value of the iterator, or `None` if there are no more values.
    """
    try:
        return next(iterator)
    except StopIteration:
        return None


def merge_sorted(left, right, comparator):
    """
    Merges two iterables sorted by `comparator` into an combined iterable that is itself sorted by `comparator`.

    :param left: Iterable first sequence. This sequence must be ordered by `comparator`.
    :param right: Iterable second sequence. This sequence must be ordered by `comparator`.
    :param comparator: Comparator function accepting two arguments and returning a negative value if the first argument
                       smaller, 0 if they are equal or a positive value otherwise.
    :return: Iterable yielding items from both inputs and still sorted by `comparator`.
    """
    left_iterator = iter(left)
    right_iterator = iter(right)
    cur_left = next_or_none(left_iterator)
    cur_right = next_or_none(right_iterator)
    while cur_left is not None or cur_right is not None:
        if cur_left is None:
            yield cur_right
            cur_right = next_or_none(right_iterator)
        elif cur_right is None or comparator(cur_left, cur_right) <= 0:
            yield cur_left
            cur_left = next_or_none(left_iterator)
        else:
            yield cur_right
            cur_right = next_or_none(right_iterator)


def merge_many_sorted(chunks, comparator):
    if len(chunks) < 0:
        return
    elif len(chunks) == 1:
        for item in chunks[0]:
            yield item
    else:
        mid = len(chunks) // 2
        left = merge_many_sorted(chunks[:mid], comparator)
        right = merge_many_sorted(chunks[mid:], comparator)
        for item in merge_sorted(left, right, comparator):
            yield item


def _merge_sort(items, comparator, start_index, end_index):
    if end_index - start_index <= 1:
        return

    mid = (start_index + end_index) // 2
    _merge_sort(items, comparator, start_index, mid)
    _merge_sort(items, comparator, mid, end_index)
    left_index = start_index
    right_index = mid
    tmp = []
    while left_index < mid or right_index < end_index:
        if left_index == mid:
            tmp.append(items[right_index])
            right_index += 1
        elif right_index == end_index or comparator(items[left_index], items[right_index]) <= 0:
            tmp.append(items[left_index])
            left_index += 1
        else:
            tmp.append(items[right_index])
            right_index += 1
    for i, x in enumerate(tmp):
        items[start_index + i] = x


def merge_sort(items, comparator):
    result = [*items]
    _merge_sort(result, comparator, 0, len(result))
    return result


def chunked_merge_sort(entries, comparator, items_per_chunk=100000):
    entry_iterator = iter(entries)
    chunk_names = []
    while True:
        chunk = []
        for _ in range(items_per_chunk):
            entry = next_or_none(entry_iterator)
            if entry is None:
                break
            else:
                chunk.append(entry)
        if len(chunk) == 0:
            break
        sorted_chunk = merge_sort(chunk, comparator)
        chunk_name = f"chunked_merge_sort.part{len(chunk_names)}"
        write_data(chunk_name, sorted_chunk)
        chunk_names.append(chunk_name)
    chunks = [read_data(name, None) for name in chunk_names]
    return merge_many_sorted(chunks, comparator)


def left_join(left, right, key, comparator=default_comparator):
    """
    Yields pairs of (left_item, right_item) joined by the key `key` ordered by `comparator`.

    Complexity:
    - Time: Theta(len(left_item) + len(right))
    - Memory: Theta(1)

    :param left: Each key value must be unique. Sorted by key.
    :param right: Key values may be repeated. Sorted by key.
    :param key:
    :param comparator:
    :return:
    """
    right_iterator = iter(right)
    cur_right = next_or_none(right_iterator)
    for cur_left in left:
        left_key = cur_left[key]
        while cur_right is not None:
            right_key = cur_right[key]
            order = comparator(right_key, left_key) < 0
            if order > 0:
                break
            else:
                if order == 0:
                    yield cur_left, cur_right
                cur_right = next_or_none(right_iterator)




if __name__ == "__main__":
    movies = read_data("meta_movies", None)


    def comparator(left, right):
        return default_comparator(left["asin"], right["asin"])


    meta_movies_asin_sorted = chunked_merge_sort(movies, comparator)

    write_data("meta_movies_asin_sorted", meta_movies_asin_sorted)
