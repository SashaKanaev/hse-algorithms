from solution import group_anagrams


def normalize(groups):
    """
    Приводит результат к единому виду,
    чтобы порядок групп и слов внутри групп
    не влиял на проверку.
    """
    return sorted(
        [sorted(group) for group in groups]
    )


def test_example():
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

    expected = [
        ["bat"],
        ["nat", "tan"],
        ["ate", "eat", "tea"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_empty_list():
    assert group_anagrams([]) == []


def test_single_word():
    assert normalize(group_anagrams(["hello"])) == [["hello"]]


def test_all_words_are_anagrams():
    strs = ["abc", "bca", "cab", "acb", "bac", "cba"]

    expected = [
        ["abc", "bca", "cab", "acb", "bac", "cba"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_no_anagrams():
    strs = ["cat", "dog", "bird", "fish"]

    expected = [
        ["cat"],
        ["dog"],
        ["bird"],
        ["fish"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_duplicate_words():
    strs = ["eat", "eat", "tea", "ate", "bat", "bat"]

    expected = [
        ["eat", "eat", "tea", "ate"],
        ["bat", "bat"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_empty_strings():
    strs = ["", "", "a", "a"]

    expected = [
        ["", ""],
        ["a", "a"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_words_with_repeated_letters():
    strs = [
        "aabb",
        "abab",
        "bbaa",
        "abba",
        "abc",
        "cab",
    ]

    expected = [
        ["aabb", "abab", "bbaa", "abba"],
        ["abc", "cab"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_different_word_lengths():
    strs = [
        "a",
        "ab",
        "ba",
        "abc",
        "bca",
        "abcd",
        "dcba",
    ]

    expected = [
        ["a"],
        ["ab", "ba"],
        ["abc", "bca"],
        ["abcd", "dcba"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_many_groups():
    strs = [
        "eat", "tea", "ate",
        "tan", "nat",
        "bat", "tab",
        "listen", "silent", "enlist",
        "evil", "vile", "veil", "live",
        "cat", "act",
        "dog",
    ]

    expected = [
        ["eat", "tea", "ate"],
        ["tan", "nat"],
        ["bat", "tab"],
        ["listen", "silent", "enlist"],
        ["evil", "vile", "veil", "live"],
        ["cat", "act"],
        ["dog"],
    ]

    assert normalize(group_anagrams(strs)) == normalize(expected)


def test_large_input():
    strs = []

    for _ in range(100):
        strs.extend([
            "abc",
            "bca",
            "cab",
            "listen",
            "silent",
            "enlist",
            "evil",
            "vile",
            "live",
        ])

    result = normalize(group_anagrams(strs))

    expected = normalize([
        ["abc", "bca", "cab"] * 100,
        ["listen", "silent", "enlist"] * 100,
        ["evil", "vile", "live"] * 100,
    ])

    assert result == expected
