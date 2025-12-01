# Advent of Code Solutions

This repository contains solutions for [Advent of Code](https://adventofcode.com) challenges, organized by year and day.

## Repository Structure

```
advent_of_code/
├── runner.py              # CLI runner script
├── year_YYYY/             # One directory per year
│   └── day_XX/            # One directory per day (01-24)
│       ├── CHALLENGE.md   # The problem statement
│       ├── solution.py    # Your solution code
│       ├── test_input.txt # Test input from the challenge
│       └── input.txt      # Challenge input (download from AoC)
```

## Quick Start

### 1. Install the Package

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 2. Create a New Challenge

Use the scaffold script to create a new challenge (e.g., 2024 Day 5):

```bash
aoc-scaffold 2024 5
```

Or manually:

```bash
mkdir -p advent_of_code/year_2024/day_05
touch advent_of_code/year_2024/day_05/{solution.py,test_input.txt,input.txt}
```

Or copy the template from an existing day:

```bash
cp -r advent_of_code/year_2024/day_01 advent_of_code/year_2024/day_05
```

### 3. Write Your Solution

Edit `advent_of_code/year_YYYY/day_XX/solution.py`. Your solution must have a `solve()` function:

```python
def solve(input_data: str) -> tuple[int, int]:
    """
    Solve the Advent of Code challenge.
    
    Args:
        input_data: The input data as a string
        
    Returns:
        A tuple of (part1_result, part2_result)
    """
    # Your solution here
    part1_result = 0
    part2_result = 0
    return part1_result, part2_result
```

### 4. Add Input Files

- **test_input.txt**: Copy the example input from the challenge description
- **input.txt**: Download your personal input from the Advent of Code website

### 5. Run Your Solution

#### Using the CLI runner (recommended):

```bash
# Run in test mode (uses test_input.txt)
aoc 2024 5 --test

# Run in challenge mode (uses input.txt)
aoc 2024 5
```

#### Or run directly:

```bash
python -m advent_of_code.runner 2024 5 --test
python -m advent_of_code.runner 2024 5
```

#### Or run the solution file directly:

```bash
python advent_of_code/year_2024/day_05/solution.py
```

## Usage Examples

```bash
# Scaffold a new challenge day
aoc-scaffold 2024 5

# Run 2024 Day 1 in test mode
aoc 2024 1 --test

# Run 2024 Day 1 in challenge mode
aoc 2024 1

# Run 2025 Day 12 in test mode
aoc 2025 12 --test
```

## Solution Template

Each `solution.py` file should follow this structure:

```python
"""
Advent of Code YYYY - Day XX

Brief description of the challenge.
"""


def solve(input_data: str) -> tuple[int, int]:
    """
    Solve the Advent of Code challenge.
    
    Args:
        input_data: The input data as a string
        
    Returns:
        A tuple of (part1_result, part2_result)
    """
    lines = input_data.strip().split("\n")
    
    # Part 1 solution
    part1_result = 0
    
    # Part 2 solution
    part2_result = 0
    
    return part1_result, part2_result


if __name__ == "__main__":
    # Allow running directly for quick testing
    import sys
    from pathlib import Path
    
    test_input_file = Path(__file__).parent / "test_input.txt"
    if test_input_file.exists():
        with open(test_input_file) as f:
            test_data = f.read().rstrip("\n")
        part1, part2 = solve(test_data)
        print(f"Part 1: {part1}")
        print(f"Part 2: {part2}")
    else:
        print("No test_input.txt found", file=sys.stderr)
```

## Tips

1. **Test First**: Always run with `--test` first to verify your solution works with the example input
2. **Input Handling**: The `input_data` string preserves the exact input format. Use `.rstrip("\n")` if you need to remove trailing newlines
3. **Return Types**: The `solve()` function should return a tuple of two values (can be `int`, `str`, etc.)
4. **Error Handling**: The runner will catch and display errors, so you can focus on solving the problem

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
ruff check .
ruff format .
```

### Type Checking

```bash
mypy advent_of_code
```

## Notes

- Most years have 24 days of challenges (Dec 1-24)
- Starting in 2025, challenges run for 12 days (Dec 1-12)
- Each challenge has two parts, typically unlocked sequentially
- Test inputs are provided in the challenge description
- Challenge inputs are personalized and must be downloaded from the website

## License

This repository is for personal use in solving Advent of Code challenges.

