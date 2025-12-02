"""Advent of Code 2025 - Day 2."""

import logging
from math import ceil, floor


logger = logging.getLogger(__name__)


class IDRange:
    """A class encapsulating the ranges for Day 2."""

    def __init__(self, id_range_str: str) -> None:
        self.start_id, self.end_id = (int(idx) for idx in id_range_str.split("-"))

    def __repr__(self) -> str:
        """Print out the qualities of the ID range."""
        return f"Start ID: {self.start_id}, End ID: {self.end_id}"

    def __contains__(self, idx: int | str) -> bool:
        """Indicate whether or not a given number is in this range."""
        if isinstance(idx, str):
            idx = int(idx)
        return idx in range(self.start_id, self.end_id + 1)

    def invalid_ids(self) -> list[int]:
        """Get the list of invalid IDs for this range.

        An invalid ID is one in which the ID is composed of a sequence of numbers that
        repeat exactly twice.
        """
        invalid_ids: list[int] = []

        start_id_len = len(str(self.start_id))
        end_id_len = len(str(self.end_id))

        start_id = self.start_id
        end_id = self.end_id

        # If all IDs in range are an odd length, then all are valid
        if start_id_len == end_id_len and start_id_len % 2 != 0:
            return invalid_ids

        # If the start ID length is odd, start at 1X where X is the number of zeros
        if start_id_len == 1:
            start_id = int("1" + ("0" * start_id_len))
        if end_id_len % 2 != 0:
            end_id = int("9" * (end_id_len - 1))

        start_id_str = str(start_id)
        start_id_half = int(start_id_str[: len(start_id_str) // 2])

        end_id_str = str(end_id)
        end_id_half = int(end_id_str[: len(end_id_str) // 2])

        for idx in range(start_id_half, end_id_half + 1):
            invalid_id = int(str(idx) * 2)
            if invalid_id in self:
                invalid_ids.append(invalid_id)

        return invalid_ids

    def invalid_ids_part2(self) -> list[int]:
        """Get the list of invalid IDs for Part 2 of Day 2.

        In this part, it's invalid if
        - The ID is in the range.
        - The ID consists entirely of a part of the ID repeats any number of times.
        """
        invalid_ids: list[int] = []

        start_id = self.start_id
        end_id = self.end_id
        start_id_len = len(str(start_id))
        end_id_len = len(str(end_id))

        # If starting ID is only one digit, then bump it to 10
        if len(str(self.start_id)) == 1:
            start_id = 10

        start_id_str = str(start_id)
        start_id_half = int(start_id_str[: floor(len(start_id_str) // 2)])

        end_id_str = str(end_id)
        end_id_half = int(end_id_str[: ceil(len(end_id_str) / 2)])

        repeat = 2
        # Only check for repeats up to the length of the max ID
        while repeat < (end_id_len + 1):
            # Pattern must occur at least twice, so we can cut our search space to this
            # range.
            for idx in range(start_id_half, end_id_half + 1):
                # Only check for this range of ID lengths
                for id_len in range(start_id_len, end_id_len + 1):
                    # Only check if a given ID length is a multiple of the repeat
                    if id_len % repeat == 0:
                        # See how long the pattern must be for this repeat and ID length
                        pattern_len = id_len // repeat
                        # Get the pattern from the ID
                        pattern = str(idx)[:pattern_len]
                        # Create the candidate ID
                        candidate = int(pattern * repeat)
                        # Only add the candidate if it's not already in the list
                        # and is in the range
                        if candidate not in invalid_ids and candidate in self:
                            invalid_ids.append(int(candidate))
            repeat += 1

        return invalid_ids


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
    id_ranges_strs = input_data.strip().split(",")

    id_ranges = [IDRange(idr) for idr in id_ranges_strs]

    sum_invalid_ids = 0
    sum_invalid_ids_part2 = 0
    for idr in id_ranges:
        invalid_id_list = idr.invalid_ids()
        sum_invalid_ids += sum(invalid_id_list)

        invalid_id_list_part2 = idr.invalid_ids_part2()
        sum_invalid_ids_part2 += sum(invalid_id_list_part2)

    # Part 1: Your solution here
    part1_result = sum_invalid_ids

    # Part 2: Your solution here
    part2_result = sum_invalid_ids_part2

    return part1_result, part2_result
