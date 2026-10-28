from itertools import permutations as itertools_permutations, product
from math import factorial
from pathlib import Path
import random
import subprocess
import sys

import pytest

from permutations import permutations


@pytest.mark.parametrize(
    "nums, expected",
    [
        ([1, 2, 3], [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
        ([0, 1], [[0, 1], [1, 0]]),
        ([1], [[1]]),
        ([], [[]]),
        ([0], [[0]]),
        ([-1, 0], [[-1, 0], [0, -1]]),
        ([3, 2, 1], [[3, 2, 1], [3, 1, 2], [2, 3, 1], [2, 1, 3], [1, 3, 2], [1, 2, 3]]),
        ([1, 1], [[1, 1]]),
        ([1, 1, 2], [[1, 1, 2], [1, 2, 1], [2, 1, 1]]),
        ([2, 1, 2], [[2, 1, 2], [2, 2, 1], [1, 2, 2]]),
        ([2, 2, 2], [[2, 2, 2]]),
        ([0, -1, 0], [[0, -1, 0], [0, 0, -1], [-1, 0, 0]]),
    ],
)
def test_known_cases(nums, expected, capsys):
    assert permutations(nums) == expected
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_number_of_permutations_for_distinct_numbers(n):
    result = permutations(list(range(n)))
    assert len(result) == factorial(n)
    assert len({tuple(row) for row in result}) == factorial(n)


def test_all_permutations_contain_original_elements():
    nums = [-3, 0, 4, 7]
    result = permutations(nums)
    assert all(sorted(row) == sorted(nums) for row in result)
    assert len(result) == 24


def test_input_list_is_not_modified():
    nums = [2, -1, 2, 0]
    original = nums.copy()
    permutations(nums)
    assert nums == original
    permutations(nums, trace=True)
    assert nums == original


def test_result_lists_are_independent():
    result = permutations([1, 2, 3])
    result[0][0] = 999
    assert result[1] == [1, 3, 2]
    assert result[-1] == [3, 2, 1]


def test_result_does_not_alias_input():
    nums = [9]
    result = permutations(nums)
    nums[0] = 100
    assert result == [[9]]
    result[0][0] = 200
    assert nums == [100]


def test_repeated_calls_are_independent(capsys):
    assert permutations([1, 2]) == [[1, 2], [2, 1]]
    assert permutations([3]) == [[3]]
    assert permutations([1, 2], trace=True) == [[1, 2], [2, 1]]
    assert capsys.readouterr().out.startswith("Вызов backtrack([])\n")
    assert permutations([]) == [[]]


def test_exhaustive_arrays_with_repetitions():
    for n in range(6):
        for nums in product([0, 1, 2], repeat=n):
            expected = [list(row) for row in dict.fromkeys(itertools_permutations(nums))]
            assert permutations(list(nums)) == expected


def test_random_cases_against_itertools():
    rng = random.Random(2026)
    for _ in range(150):
        nums = [rng.randint(-3, 3) for _ in range(rng.randint(0, 7))]
        expected = [list(row) for row in dict.fromkeys(itertools_permutations(nums))]
        assert permutations(nums) == expected


def test_many_duplicates():
    nums = [1] * 5 + [2] * 5
    result = permutations(nums)
    assert len(result) == 252
    assert len({tuple(row) for row in result}) == 252
    assert all(row.count(1) == 5 and row.count(2) == 5 for row in result)


def test_trace_two_elements_exact_output(capsys):
    assert permutations([0, 1], trace=True) == [[0, 1], [1, 0]]
    assert capsys.readouterr().out.splitlines() == [
        "Вызов backtrack([])",
        "    Вызов backtrack([0])",
        "        Вызов backtrack([0, 1])",
        "        Возврат backtrack([0, 1]) = 1",
        "    Возврат backtrack([0]) = 1",
        "    Вызов backtrack([1])",
        "        Вызов backtrack([1, 0])",
        "        Возврат backtrack([1, 0]) = 1",
        "    Возврат backtrack([1]) = 1",
        "Возврат backtrack([]) = 2",
    ]


def test_trace_three_elements_call_stack(capsys):
    assert len(permutations([1, 2, 3], trace=True)) == 6
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 32
    assert lines[0] == "Вызов backtrack([])"
    assert lines[-1] == "Возврат backtrack([]) = 6"
    for index, first in enumerate([1, 2, 3]):
        assert f"    Вызов backtrack([{first}])" in lines
        assert f"    Возврат backtrack([{first}]) = 2" in lines
    assert lines[3] == "            Вызов backtrack([1, 2, 3])"
    assert lines[4] == "            Возврат backtrack([1, 2, 3]) = 1"
    assert len([line for line in lines if "Вызов" in line]) == 16
    assert len([line for line in lines if "Возврат" in line]) == 16


def test_trace_empty_array(capsys):
    assert permutations([], trace=True) == [[]]
    assert capsys.readouterr().out.splitlines() == [
        "Вызов backtrack([])",
        "Возврат backtrack([]) = 1",
    ]


def test_trace_duplicates_skip_repeated_branches(capsys):
    assert permutations([1, 1, 2], trace=True) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Вызов backtrack([])"
    assert lines[-1] == "Возврат backtrack([]) = 3"
    assert lines.count("    Вызов backtrack([1])") == 1
    assert lines.count("    Вызов backtrack([2])") == 1
    assert len([line for line in lines if "            Возврат backtrack" in line]) == 3


def test_trace_indentation_matches_depth(capsys):
    permutations([1, 2, 3], trace=True)
    lines = capsys.readouterr().out.splitlines()
    depth = 0
    for line in lines:
        spaces = len(line) - len(line.lstrip(" "))
        assert spaces % 4 == 0
        if "Вызов " in line:
            assert spaces == 4 * depth
            depth += 1
        else:
            depth -= 1
            assert spaces == 4 * depth
    assert depth == 0


def test_no_trace_by_default(capsys):
    permutations([1, 2, 3])
    assert capsys.readouterr().out == ""


def run_cli(text, *args):
    return subprocess.run(
        [sys.executable, "-m", "homework_5.permutations.permutations", *args],
        input=text,
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
    )


@pytest.mark.parametrize(
    "text, expected",
    [
        ("[1, 2, 3]\n", "[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]"),
        ("[0, 1]\n", "[[0, 1], [1, 0]]"),
        ("[1]\n", "[[1]]"),
        ("[]\n", "[[]]"),
    ],
)
def test_command_line(text, expected):
    process = run_cli(text)
    assert process.returncode == 0, process.stderr
    assert process.stdout.strip() == expected
    assert process.stderr == ""


def test_command_line_as_script():
    program = Path(__file__).with_name("permutations.py")
    process = subprocess.run(
        [sys.executable, str(program)],
        input="[0, 1]\n",
        capture_output=True,
        text=True,
        check=True,
    )
    assert process.stdout.strip() == "[[0, 1], [1, 0]]"
    assert process.stderr == ""


def test_command_line_trace_as_script():
    program = Path(__file__).with_name("permutations.py")
    process = subprocess.run(
        [sys.executable, str(program), "--trace"],
        input="[0, 1]\n",
        capture_output=True,
        text=True,
        check=True,
    )
    lines = process.stdout.splitlines()
    assert lines[0] == "Вызов backtrack([])"
    assert lines[-1] == "[[0, 1], [1, 0]]"
    assert process.stderr == ""


def test_command_line_trace():
    process = run_cli("[0, 1]\n", "--trace")
    assert process.returncode == 0, process.stderr
    assert process.stdout.splitlines()[0] == "Вызов backtrack([])"
    assert process.stdout.splitlines()[-2] == "Возврат backtrack([]) = 2"
    assert process.stdout.splitlines()[-1] == "[[0, 1], [1, 0]]"


def test_invalid_command_line_input():
    process = run_cli("(1, 2, 3)\n")
    assert process.returncode != 0
    assert "Ожидается список целых чисел" in process.stderr


def test_import_has_no_output():
    process = subprocess.run(
        [sys.executable, "-c", "from homework_5.permutations.permutations import permutations"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
        check=True,
    )
    assert process.stdout == ""
    assert process.stderr == ""
