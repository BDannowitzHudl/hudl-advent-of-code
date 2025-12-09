"""Advent of Code 2025 - Day 5."""

import logging
import time


logger = logging.getLogger(__name__)


class IDRange:
    """A range of IDs."""

    def __init__(self, range_str: str) -> None:
        range_vals = range_str.split("-")
        if len(range_vals) != 2:  # noqa: PLR2004
            msg = f"Expected N-N for range. Got {range_str}."
            raise ValueError(msg)
        self.beginning = int(range_vals[0])
        self.end = int(range_vals[1])

    def __contains__(self, idx: int) -> bool:
        """Is the ID FRESH."""
        return self.beginning <= idx <= self.end

    def __len__(self) -> int:
        """Get the inclusive length of the range."""
        return self.end - self.beginning + 1


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
    lines = input_data.strip().split("\n")
    id_ranges = [IDRange(s) for s in lines if "-" in s]
    id_list = [int(s) for s in lines if len(s) > 0 and "-" not in s]

    # Part 1: Your solution here
    start_time = time.perf_counter()
    fresh_count = 0
    for idx in id_list:
        for idr in id_ranges:
            if idx in idr:
                fresh_count += 1
                break

    part1_result = fresh_count
    part1_time = time.perf_counter() - start_time
    logger.info("Part 1: %s (%.4fs)", part1_result, part1_time)

    # Part 2: Your solution here
    start_time = time.perf_counter()
    id_ranges = sorted(id_ranges, key=lambda idr: idr.beginning)
    fresh_count = 0
    last_interval = None
    for idr in id_ranges:
        # First IDR
        if last_interval is None:
            fresh_count += len(idr)
            last_interval = idr

        # If disjoint
        elif idr.beginning > last_interval.end:
            fresh_count += len(idr)

        # Any overlap
        elif idr.beginning <= last_interval.end:
            # Only add new values
            if idr.end > last_interval.end:
                fresh_count += idr.end - last_interval.end
            else:
                continue

        last_interval = idr

    part2_result = fresh_count
    part2_time = time.perf_counter() - start_time
    logger.info("Part 2: %s (%.4fs)", part2_result, part2_time)

    return part1_result, part2_result
