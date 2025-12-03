"""Advent of Code 2025 - Day 3."""

import logging
import time


logger = logging.getLogger(__name__)


class PowerBank:
    """A class encapsulating the power bank for Day 3."""

    def __init__(self, bank_str: str) -> None:
        """Initialize the power bank."""
        self.bank_str = bank_str
        self.bank = [int(digit) for digit in bank_str]

    def __repr__(self) -> str:
        """Print out the qualities of the power bank."""
        return f"PowerBank(bank_str={self.bank_str})"

    def max_joltage(self, num_batteries: int) -> int:
        """Get the maximum joltage possible from the bank.

        Parameters
        ----------
        num_batteries: int
            The number of batteries to turn on

        Returns
        -------
        int
            The maximum joltage possible from the bank.
        """
        max_bank, _ = self._max_joltage(
            current_bank="",
            remaining_bank=self.bank_str,
            remaining_batteries=num_batteries,
        )
        return int(max_bank)

    def _max_joltage(
        self, current_bank: str, remaining_bank: str, remaining_batteries: int
    ) -> tuple[str, str]:
        """Recursively get the max power bank consisting of N batteries.

        The order in the bank must be respected.

        Parameters
        ----------
        current_bank: str
            The current bank of batteries as a single string
        remaining_bank: str
            The remaining bank of batteries as a single string
        remaining_batteries: int
            The number of batteries still needed

        Returns
        -------
        tuple[str, str]
            A tuple of (the current bank of batteries, the remaining bank of batteries)
        """
        # If no more batteries to collect, then we're done!
        if remaining_batteries == 0:
            return current_bank, remaining_bank

        # Need to know the number of remaining batteries
        bank_len = len(remaining_bank)
        # Need to know the unique battery capacities
        battery_set = set(remaining_bank)
        # Initialize the index (start at the first one)
        max_battery_index = 0
        while True:
            # Pick the largest capacity
            max_battery = max(battery_set)
            # Remove it from the pool
            battery_set.remove(max_battery)
            # Get the index of the first-occurring battery with this capacity
            max_battery_index = remaining_bank.index(max_battery)
            # As long as there are enough batteries following it, we want it!
            if (bank_len - max_battery_index) >= remaining_batteries:
                # Update the current bank, remaining bank, and
                # number of batteries still needed, then call it again!
                current_bank = current_bank + max_battery
                remaining_bank = remaining_bank[max_battery_index + 1 :]
                remaining_batteries -= 1
                return self._max_joltage(
                    current_bank=current_bank,
                    remaining_bank=remaining_bank,
                    remaining_batteries=remaining_batteries,
                )


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

    power_banks = [PowerBank(bank_str) for bank_str in lines]

    start_time = time.perf_counter()
    max_joltages = [
        power_bank.max_joltage(num_batteries=2) for power_bank in power_banks
    ]
    part1_result = sum(max_joltages)
    part1_time = time.perf_counter() - start_time
    logger.info("Part 1: %s (%.4fs)", part1_result, part1_time)

    start_time = time.perf_counter()
    max_joltages = [
        power_bank.max_joltage(num_batteries=12) for power_bank in power_banks
    ]
    part2_result = sum(max_joltages)
    part2_time = time.perf_counter() - start_time
    logger.info("Part 2: %s (%.4fs)", part2_result, part2_time)

    return part1_result, part2_result
