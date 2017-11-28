def default_comparator(left, right):
    """
    Comparator function using the comparison operators defined on the compared objects.
    It returns `-1` if `left < right`, `0` if `left == right` and `1` otherwise.
    This can be used for custom sorting functions.

    :param left: Left element to compare
    :param right: Right element to compare
    :return: Comparison result
    """
    if left < right:
        return -1
    elif left == right:
        return 0
    else:
        return 1
