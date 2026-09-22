import pytest

from merge_lists import (
    ListNode,
    merge_two_lists_with_dummy,
    merge_two_lists_without_dummy,
)


def build_list(values):
    if not values:
        return None

    head = ListNode(values[0])
    current = head

    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next

    return head


def to_list(head):
    result = []

    while head:
        result.append(head.val)
        head = head.next

    return result


merge_functions = [
    merge_two_lists_with_dummy,
    merge_two_lists_without_dummy,
]


@pytest.mark.parametrize("merge_func", merge_functions)
@pytest.mark.parametrize(
    "values1, values2, expected",
    [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [1, 2, 3], [1, 2, 3]),
        ([1, 2, 3], [], [1, 2, 3]),
        ([1], [2], [1, 2]),
        ([2], [1], [1, 2]),
        ([1, 2, 3], [10, 20, 30], [1, 2, 3, 10, 20, 30]),
        ([10, 20, 30], [1, 2, 3], [1, 2, 3, 10, 20, 30]),
        ([1, 4, 7, 10], [2, 3, 8, 9], [1, 2, 3, 4, 7, 8, 9, 10]),
        ([1, 1, 3], [1, 2, 2], [1, 1, 1, 2, 2, 3]),
        ([-10, -3, 5], [-8, 0, 7], [-10, -8, -3, 0, 5, 7]),
    ],
)
def test_merge_lists(merge_func, values1, values2, expected):
    list1 = build_list(values1)
    list2 = build_list(values2)

    result = merge_func(list1, list2)

    assert to_list(result) == expected
