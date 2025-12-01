#!/usr/bin/env python3
"""
Advent of Code Runner.

Run solutions for specific year/day combinations in test or challenge mode.
"""

import argparse
import importlib
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def get_solution_module(year: int, day: int) -> tuple[str, Path]:
    """Get the solution module path and input file directory."""
    day_str = f"day_{day:02d}"
    year_str = f"year_{year}"
    module_name = f"advent_of_code.{year_str}.{day_str}.solution"
    input_dir = Path(__file__).parent / year_str / day_str
    return module_name, input_dir


def run_solution(year: int, day: int, test_mode: bool = False) -> None:
    """Run a solution for a specific year and day."""
    module_name, input_dir = get_solution_module(year, day)

    # Determine input file
    if test_mode:
        input_file = input_dir / "test_input.txt"
        mode_name = "TEST"
    else:
        input_file = input_dir / "input.txt"
        mode_name = "CHALLENGE"

    if not input_file.exists():
        logger.error("Input file not found: %s", input_file)
        sys.exit(1)

    # Read input
    with input_file.open() as f:
        input_data = f.read().rstrip("\n")

    # Import and run solution
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        logger.exception(
            "Solution module not found: %s. Create %s to solve this challenge.",
            module_name,
            input_dir / "solution.py",
        )
        sys.exit(1)

    if not hasattr(module, "solve"):
        logger.error(
            "Solution module must have a 'solve(input_data: str) -> tuple' function"
        )
        sys.exit(1)

    logger.info("Running %d Day %d (%s mode)", year, day, mode_name)
    logger.info("Input file: %s", input_file)
    logger.info("-" * 60)

    try:
        part1_result, part2_result = module.solve(input_data)
        logger.info("Part 1: %s", part1_result)
        logger.info("Part 2: %s", part2_result)
    except Exception:
        logger.exception("Error running solution")
        sys.exit(1)


def main() -> None:
    """Run the Advent of Code runner."""
    parser = argparse.ArgumentParser(
        description="Run Advent of Code solutions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 2024 1              # Run 2024 Day 1 in challenge mode
  %(prog)s 2024 1 --test       # Run 2024 Day 1 in test mode
  %(prog)s 2025 12 --test      # Run 2025 Day 12 in test mode
        """.strip(),
    )
    parser.add_argument("year", type=int, help="Year of the challenge (e.g., 2024)")
    parser.add_argument(
        "day",
        type=int,
        help="Day of the challenge (1-24 for most years, 1-12 for 2025+)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode (uses test_input.txt instead of input.txt)",
    )

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
    )

    max_day = 24
    if args.day < 1 or args.day > max_day:
        logger.warning("Day %d is outside typical range (1-%d)", args.day, max_day)

    run_solution(args.year, args.day, test_mode=args.test)


if __name__ == "__main__":
    main()
