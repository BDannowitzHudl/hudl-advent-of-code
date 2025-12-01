#!/usr/bin/env python3
"""
Scaffold a new Advent of Code challenge day.

Creates the directory structure and template files for a new challenge.
"""

import argparse
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


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
    part1_result = 0

    # Part 2: Your solution here
    part2_result = 0

    return part1_result, part2_result

'''
    (day_dir / "solution.py").write_text(solution_template)

    # Create empty input files
    (day_dir / "test_input.txt").write_text(
        "# Example test input\n# Replace with actual test input from the challenge\n"
    )
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
    logger.info("  2. Download challenge input to %s", day_dir / "input.txt")
    logger.info("  3. Implement your solution in %s", day_dir / "solution.py")
    logger.info("  4. Run with: aoc %d %d --test", year, day)


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
