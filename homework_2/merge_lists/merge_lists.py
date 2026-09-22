class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists_with_dummy(
    list1: ListNode | None,
    list2: ListNode | None
) -> ListNode | None:
    dummy = ListNode(-1)
    current = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists_with_dummy(
    list1: ListNode | None,
    list2: ListNode | None
) -> ListNode | None:
    dummy = ListNode(-1)
    current = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next

        current = current.next

    current.next = list1 if list1 else list2

    return dummy.next


def merge_two_lists_without_dummy(
    list1: ListNode | None,
    list2: ListNode | None
) -> ListNode | None:
    if not list1:
        return list2

    if not list2:
        return list1

    if list1.val <= list2.val:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    current = head

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next

        current = current.next

    current.next = list1 if list1 else list2

    return head
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next

        current = current.next

    current.next = list1 if list1 else list2

    return dummy.next


def merge_two_lists_without_dummy(
    list1: ListNode | None,
    list2: ListNode | None
) -> ListNode | None:
    if not list1:
        return list2

    if not list2:
        return list1

    if list1.val <= list2.val:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    current = head

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next

        current = current.next

    current.next = list1 if list1 else list2

    return head
