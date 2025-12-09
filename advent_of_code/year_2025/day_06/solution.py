"""Advent of Code 2025 - Day 6."""

import logging
import time
from functools import reduce
from operator import add, mul


logger = logging.getLogger(__name__)


def part1(lines: list[str]) -> int:
    """Perform part 1 of the challenge."""
    part1_result = 0
    rank = len(lines)
    operands = []
    operators = []
    operator_functions = []
    for ix, line in enumerate(lines):
        line = " ".join(line.split())  # noqa: PLW2901
        if ix + 1 == rank:
            operators = line.split(" ")
            for operator in operators:
                if operator == "+":
                    operator_functions.append(add)
                elif operator == "*":
                    operator_functions.append(mul)
        else:
            operands.append([int(s) for s in line.split(" ")])
    for i in range(len(operators)):
        part1_result += reduce(operator_functions[i], [int(o[i]) for o in operands])
    return part1_result


def part2(lines: list[str]) -> int:
    """Perform part 1 of the challenge."""
    part2_result = 0
    file = len(lines[0])

    nums: list[int] = []
    op = None
    for i in range(file):
        if all(line[i] == " " for line in lines):
            if op is None:
                msg = "op is None!"
                raise ValueError(msg)
            part2_result += reduce(op, nums)
            nums = []
            op = None
        else:
            op_str = lines[-1][i]
            if op_str == "+":
                op = add
            elif op_str == "*":
                op = mul
            num_str_list = [line[i] for line in lines[:-1]]
            num_str = "".join(num_str_list)
            nums.append(int(num_str.strip()))
    if op is not None:
        part2_result += reduce(op, nums)
    return part2_result


def solve(input_data: str) -> tuple[int, int]:
    """
    Solve the Advent of Code challenge.

    Parameters
    ----------
    input_data: str
        The input data as a string

    Returns
    -------
    tuple[int, int]
        A tuple of (part1_result, part2_result)
    """
    # Part 1: Your solution here
    start_time = time.perf_counter()
    lines = input_data.split("\n")
    part1_result = part1(lines)
    part1_time = time.perf_counter() - start_time
    logger.info("Part 1: %s (%.4fs)", part1_result, part1_time)

    # Part 2: Your solution here
    start_time = time.perf_counter()
    lines = input_data.split("\n")
    part2_result = part2(lines)
    part2_time = time.perf_counter() - start_time
    logger.info("Part 2: %s (%.4fs)", part2_result, part2_time)

    return part1_result, part2_result
