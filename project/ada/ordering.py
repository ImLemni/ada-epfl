def natural_comparator(left, right):
    """
    Comparator for elements of a totally ordered set using the default comparators.

    :param left:
    :param right:
    :return:
    """
    if left < right:
        return -1
    elif left == right:
        return 0
    else:
        return 1
