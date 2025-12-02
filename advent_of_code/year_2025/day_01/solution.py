"""Advent of Code 2025 - Day 1."""

import logging
import time


logger = logging.getLogger(__name__)


def turn(position: int, direction: str, distance: int) -> int:
    """Turn the dial in the given direction for the given distance.

    Parameters
    ----------
    position: int
        The current position of the dial
    direction: str
        The direction to turn the dial
    distance: int
        The distance to turn the dial

    Returns
    -------
    int
        The new position of the dial
    """
    if direction == "L":
        return (position - distance) % 100
    return (position + distance) % 100


def turn_part2(position: int, direction: str, distance: int) -> tuple[int, int]:
    """Turn the dial in the given direction for the given distance.

    Return the position it ended at along with the number of times it pointed at 0.

    Parameters
    ----------
    position: int
        The current position of the dial
    direction: str
        The direction to turn the dial
    distance: int
        The distance to turn the dial

    Returns
    -------
    tuple[int, int]
        The new position of the dial and the number of times it pointed at 0
    """
    # Don't fall for its tricks! This has got to happen in the real input!
    if distance == 0:
        return position, 0

    zeros = 0

    # Anything over 100 is gravy. Only turn it by the modulo.
    zeros += distance // 100
    distance = distance % 100

    if direction == "L":
        # If it goes below 0, that's another zero.
        if position - distance < 0 and position != 0:
            zeros += 1
        position = (position - distance) % 100
        # If it ends up on 0 after the modulo, add another zero.
        if position == 0:
            zeros += 1
    else:
        # If it goes above 99, that's another zero.
        if position + distance > 99:  # noqa: PLR2004
            zeros += 1
        position = (position + distance) % 100
    return position, zeros


def solve(input_data: str) -> tuple[int, int]:
    """
    Solve the Advent of Code challenge.

    Parameters
    ----------
    input_data: str
        The input data as a string

    Returns
    -------
        A tuple of (part1_result, part2_result)
    """
    lines = input_data.strip().split("\n")

    # Part 1
    start_time = time.perf_counter()
    position = 50
    part1_zeros = 0

    for line in lines:
        direction, distance = line[0], int(line[1:])
        position = turn(position, direction, distance)
        if position == 0:
            part1_zeros += 1

    part1_result = part1_zeros
    part1_time = time.perf_counter() - start_time
    logger.info("Part 1: %s (%.4fs)", part1_result, part1_time)

    # Part 2
    start_time = time.perf_counter()
    position = 50
    part2_zeros = 0

    for line in lines:
        direction, distance = line[0], int(line[1:])
        position, zeros = turn_part2(position, direction, distance)
        part2_zeros += zeros

    part2_result = part2_zeros
    part2_time = time.perf_counter() - start_time
    logger.info("Part 2: %s (%.4fs)", part2_result, part2_time)

    return part1_result, part2_result
