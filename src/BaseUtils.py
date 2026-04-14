import logging
from typing import Dict, Tuple

from pxr import Gf, Sdf


def TimeExecution(function):
    """
    Records the amount of time it takes to execute the input function
    """
    def wrapper(*args, **kwargs):
        import time

        start: float = time.perf_counter()
        function(*args, **kwargs)
        end: float = time.perf_counter()
        print(f"{(end - start):.5f}s")

    return wrapper

def TestMultipleExecutions(numTests: int = 1, execute: bool = True):
    """
    Executes the function a given number of times, returning information in the process

    :param numTests: The amount of times the function will be executed.
    :param execute:  Enables or disables the decorator.
    """
    def inner(function):
        def wrapper(*args, **kwargs):
            import time

            overallTime: float = 0
            for i in range(numTests):
                i += 1
                start: float = time.perf_counter()
                function(*args, **kwargs)
                end: float = time.perf_counter()
                overallTime += (end - start)
                print(f"Test number: {i} | Execution time: {(end - start):.5f}s")

            print(f"\nAverage execution time: {(overallTime / numTests):.5f}s")

        return wrapper if execute else None
    return inner

def ConvertStringToSdfPath(path: str | Sdf.Path) -> Sdf.Path:
    """
    Converts the given string to a Sdf.Path type or just returns the string if it's already a Sdf.Path

    :param path: The input path to convert or return.

    :return:     The converted path or the input path depending on it's input data type.
    """
    if not isinstance(path, str) and not isinstance(path, Sdf.Path):
        raise TypeError("Input path must be of type string or Sdf.Path")

    path: Sdf.Path = path if isinstance(path, Sdf.Path) else Sdf.Path(path)
    if not Sdf.Path.IsValidPathString(path.pathString):
        raise TypeError("Input path is not a valid Sdf.Path, must remove illegal characters before continuing")

    return path
