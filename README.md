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

Edit `advent_of_code/year_YYYY/day_XX/solution.py`. Your solution must have a `solve()` function that returns a tuple of `(part1_result, part2_result)`.

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

