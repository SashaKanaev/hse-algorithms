from pathlib import Path
from math import factorial as math_factorial
import subprocess
import sys

import pytest

from tracer import factorial, tracer


def test_factorial_example(capsys):
    assert factorial(4) == 24
    assert capsys.readouterr().out.splitlines() == [
        "Вызов factorial(4)",
        "    Вызов factorial(3)",
        "        Вызов factorial(2)",
        "            Вызов factorial(1)",
        "            Возврат factorial(1) = 1",
        "        Возврат factorial(2) = 2",
        "    Возврат factorial(3) = 6",
        "Возврат factorial(4) = 24",
    ]


@pytest.mark.parametrize("n, expected", [(0, 1), (1, 1), (2, 2), (5, 120), (8, 40320)])
def test_factorial_results(n, expected, capsys):
    assert factorial(n) == expected
    output = capsys.readouterr().out.splitlines()
    assert output[0] == f"Вызов factorial({n})"
    assert output[-1] == f"Возврат factorial({n}) = {expected}"
    assert len(output) == 2 * max(n, 1)


def test_each_depth_has_matching_return(capsys):
    factorial(12)
    lines = capsys.readouterr().out.splitlines()
    calls = lines[:12]
    returns = lines[12:]
    assert len(lines) == 24
    for depth, line in enumerate(calls):
        assert line == "    " * depth + f"Вызов factorial({12 - depth})"
    for index, line in enumerate(returns):
        n = index + 1
        assert line == "    " * (11 - index) + f"Возврат factorial({n}) = {math_factorial(n)}"


def test_empty_arguments(capsys):
    @tracer
    def answer():
        return 42

    assert answer() == 42
    assert capsys.readouterr().out.splitlines() == [
        "Вызов answer()",
        "Возврат answer() = 42",
    ]


def test_positional_and_keyword_arguments(capsys):
    @tracer
    def combine(a, b=0, text=""):
        return f"{text}{a + b}"

    assert combine(2, b=3, text="итог: ") == "итог: 5"
    assert capsys.readouterr().out.splitlines() == [
        "Вызов combine(2, b=3, text='итог: ')",
        "Возврат combine(2, b=3, text='итог: ') = 'итог: 5'",
    ]


@pytest.mark.parametrize("result", [None, True, False, 0, "слово", [1, 2], {"a": 1}])
def test_return_value_and_representation(result, capsys):
    @tracer
    def return_value():
        return result

    assert return_value() == result
    assert capsys.readouterr().out.splitlines() == [
        "Вызов return_value()",
        f"Возврат return_value() = {result!r}",
    ]


def test_branching_recursion(capsys):
    @tracer
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    assert fibonacci(3) == 2
    assert capsys.readouterr().out.splitlines() == [
        "Вызов fibonacci(3)",
        "    Вызов fibonacci(2)",
        "        Вызов fibonacci(1)",
        "        Возврат fibonacci(1) = 1",
        "        Вызов fibonacci(0)",
        "        Возврат fibonacci(0) = 0",
        "    Возврат fibonacci(2) = 1",
        "    Вызов fibonacci(1)",
        "    Возврат fibonacci(1) = 1",
        "Возврат fibonacci(3) = 2",
    ]


def test_mutual_recursion_shared_depth(capsys):
    @tracer
    def even(n):
        return True if n == 0 else odd(n - 1)

    @tracer
    def odd(n):
        return False if n == 0 else even(n - 1)

    assert even(3) is False
    assert capsys.readouterr().out.splitlines() == [
        "Вызов even(3)",
        "    Вызов odd(2)",
        "        Вызов even(1)",
        "            Вызов odd(0)",
        "            Возврат odd(0) = False",
        "        Возврат even(1) = False",
        "    Возврат odd(2) = False",
        "Возврат even(3) = False",
    ]


def test_separate_calls_start_at_depth_zero(capsys):
    factorial(2)
    factorial(1)
    lines = capsys.readouterr().out.splitlines()
    assert lines == [
        "Вызов factorial(2)",
        "    Вызов factorial(1)",
        "    Возврат factorial(1) = 1",
        "Возврат factorial(2) = 2",
        "Вызов factorial(1)",
        "Возврат factorial(1) = 1",
    ]


def test_error_is_reported_and_reraised(capsys):
    with pytest.raises(ValueError, match="non-negative"):
        factorial(-1)
    assert capsys.readouterr().out.splitlines() == [
        "Вызов factorial(-1)",
        "Ошибка factorial(-1): ValueError: n must be non-negative",
    ]


def test_error_during_recursion_resets_depth(capsys):
    @tracer
    def descend(n):
        if n == 0:
            raise LookupError("not found")
        return descend(n - 1)

    with pytest.raises(LookupError, match="not found"):
        descend(2)
    assert capsys.readouterr().out.splitlines() == [
        "Вызов descend(2)",
        "    Вызов descend(1)",
        "        Вызов descend(0)",
        "        Ошибка descend(0): LookupError: not found",
        "    Ошибка descend(1): LookupError: not found",
        "Ошибка descend(2): LookupError: not found",
    ]
    assert factorial(1) == 1
    assert capsys.readouterr().out.splitlines() == [
        "Вызов factorial(1)",
        "Возврат factorial(1) = 1",
    ]


def test_caught_error_allows_outer_function_to_return(capsys):
    @tracer
    def fail():
        raise ValueError("bad")

    @tracer
    def recover():
        try:
            fail()
        except ValueError:
            return "ok"

    assert recover() == "ok"
    assert capsys.readouterr().out.splitlines() == [
        "Вызов recover()",
        "    Вызов fail()",
        "    Ошибка fail(): ValueError: bad",
        "Возврат recover() = 'ok'",
    ]


def test_original_function_does_not_change_arguments(capsys):
    @tracer
    def collect(items, extra):
        return items + extra

    items = [1, 2]
    extra = [3]
    assert collect(items, extra) == [1, 2, 3]
    assert items == [1, 2]
    assert extra == [3]
    assert capsys.readouterr().out.splitlines() == [
        "Вызов collect([1, 2], [3])",
        "Возврат collect([1, 2], [3]) = [1, 2, 3]",
    ]


def test_metadata_is_preserved():
    @tracer
    def sample(value: int) -> int:
        """Описание функции."""
        return value

    assert sample.__name__ == "sample"
    assert sample.__doc__ == "Описание функции."
    assert sample.__annotations__ == {"value": int, "return": int}
    assert sample.__wrapped__(5) == 5


def test_returns_original_result_not_text(capsys):
    original = object()

    @tracer
    def get_object():
        return original

    assert get_object() is original
    assert "Возврат get_object() = " in capsys.readouterr().out


def test_command_line_example():
    program = Path(__file__).with_name("tracer.py")
    process = subprocess.run(
        [sys.executable, str(program)],
        capture_output=True,
        text=True,
        check=True,
    )
    assert process.stderr == ""
    assert process.stdout.splitlines() == [
        "Вызов factorial(4)",
        "    Вызов factorial(3)",
        "        Вызов factorial(2)",
        "            Вызов factorial(1)",
        "            Возврат factorial(1) = 1",
        "        Возврат factorial(2) = 2",
        "    Возврат factorial(3) = 6",
        "Возврат factorial(4) = 24",
    ]


def test_import_does_not_run_demo():
    folder = Path(__file__).parent
    process = subprocess.run(
        [sys.executable, "-c", "import tracer"],
        cwd=folder,
        capture_output=True,
        text=True,
        check=True,
    )
    assert process.stdout == ""
    assert process.stderr == ""


def test_deep_recursion_for_presentation(capsys):
    @tracer
    def count(n):
        if n == 0:
            return 0
        return count(n - 1) + 1

    assert count(100) == 100
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 202
    assert lines[0] == "Вызов count(100)"
    assert lines[100] == "    " * 100 + "Вызов count(0)"
    assert lines[101] == "    " * 100 + "Возврат count(0) = 0"
    assert lines[-1] == "Возврат count(100) = 100"
