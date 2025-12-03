#!/usr/bin/env python3
"""
Scaffold a new Advent of Code challenge day.

Creates the directory structure and template files for a new challenge.
"""

import argparse
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def fetch_input_data(year: int, day: int) -> str:
    """Fetch input data from Advent of Code website.

    Parameters
    ----------
    year: int
        The year of the challenge
    day: int
        The day of the challenge

    Returns
    -------
    str
        The input data as a string, or empty string if fetch fails
    """
    try:
        session_token = os.getenv("AOC_SESSION_TOKEN")
        if not session_token:
            raise RuntimeError("AOC_SESSION_TOKEN environment variable not set.")

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        response = requests.get(url, cookies={"session": session_token}, timeout=10)

        if not response.ok:
            raise RuntimeError(
                f"Failed to fetch input data from {url}: {response.status_code} {response.reason}"
            )

        logger.info("Successfully loaded input data for AoC %d Day %d", year, day)
        return response.text

    except Exception as e:
        logger.error("Error fetching input data: %s", e)
        return ""


def scaffold_day(year: int, day: int) -> None:
    """Create the directory structure and template files for a new day."""
    year_str = f"year_{year}"
    day_str = f"day_{day:02d}"

    base_dir = Path(__file__).parent
    year_dir = base_dir / year_str
    day_dir = year_dir / day_str

    if day_dir.exists():
        logger.warning("%s already exists. Skipping creation.", day_dir)
        return

    # Create directories
    day_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py for year if it doesn't exist
    (year_dir / "__init__.py").touch(exist_ok=True)

    # Create __init__.py for day
    (day_dir / "__init__.py").write_text("# Day {day} solution\n")

    # Create solution.py template
    solution_template = f'''"""Advent of Code {year} - Day {day}."""

import logging
import time


logger = logging.getLogger(__name__)


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
    lines = input_data.strip().split("\\n")  # noqa: F841

    # Part 1: Your solution here
    start_time = time.perf_counter()
    part1_result = 0
    part1_time = time.perf_counter() - start_time
    logger.info("Part 1: %s (%.4fs)", part1_result, part1_time)

    # Part 2: Your solution here
    start_time = time.perf_counter()
    part2_result = 0
    part2_time = time.perf_counter() - start_time
    logger.info("Part 2: %s (%.4fs)", part2_result, part2_time)

    return part1_result, part2_result

'''
    (day_dir / "solution.py").write_text(solution_template)

    # Create empty test input file
    (day_dir / "test_input.txt").write_text(
        "# Example test input\n# Replace with actual test input from the challenge\n"
    )

    # Fetch and write input.txt
    input_data = fetch_input_data(year, day)
    if input_data:
        (day_dir / "input.txt").write_text(input_data)
    else:
        (day_dir / "input.txt").write_text(
            "# Challenge input goes here\n# Download from https://adventofcode.com\n"
        )

    # Create empty CHALLENGE.md file
    (day_dir / "CHALLENGE.md").write_text("")

    logger.info("Created %s", day_dir)
    logger.info("  - solution.py")
    logger.info("  - test_input.txt")
    logger.info("  - input.txt")
    logger.info("  - CHALLENGE.md")
    logger.info("")
    logger.info("Next steps:")
    logger.info("  1. Add test input to %s", day_dir / "test_input.txt")
    step = 2
    if not input_data:
        logger.info("  %d. Set AOC_SESSION_TOKEN in .env file and re-run scaffold to fetch input", step)
        step += 1
    logger.info("  %d. Implement your solution in %s", step, day_dir / "solution.py")
    logger.info("  %d. Run with: aoc %d %d --test", step + 1, year, day)


def main() -> None:
    """Run the scaffold script."""
    parser = argparse.ArgumentParser(
        description="Scaffold a new Advent of Code challenge day",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 2024 1    # Create structure for 2024 Day 1
  %(prog)s 2025 12   # Create structure for 2025 Day 12
        """.strip(),
    )
    parser.add_argument("year", type=int, help="Year of the challenge (e.g., 2024)")
    parser.add_argument(
        "day",
        type=int,
        help="Day of the challenge (1-24 for most years, 1-12 for 2025+)",
    )

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
    )

    max_day = 24
    if args.day < 1 or args.day > max_day:
        logger.warning("Day %d is outside typical range (1-%d)", args.day, max_day)

    scaffold_day(args.year, args.day)


if __name__ == "__main__":
    main()
