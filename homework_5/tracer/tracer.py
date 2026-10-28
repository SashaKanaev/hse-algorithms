from contextvars import ContextVar
from functools import wraps


_depth = ContextVar("tracer_depth", default=0)


def tracer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        depth = _depth.get()
        arguments = [repr(arg) for arg in args]
        arguments.extend(f"{key}={value!r}" for key, value in kwargs.items())
        call = f"{func.__name__}({', '.join(arguments)})"
        indent = "    " * depth

        print(f"{indent}Вызов {call}")
        token = _depth.set(depth + 1)

        try:
            result = func(*args, **kwargs)
        except Exception as error:
            print(f"{indent}Ошибка {call}: {type(error).__name__}: {error}")
            raise
        else:
            print(f"{indent}Возврат {call} = {result!r}")
            return result
        finally:
            _depth.reset(token)

    return wrapper


@tracer
def factorial(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return 1
    return n * factorial(n - 1)


if __name__ == "__main__":
    factorial(4)
