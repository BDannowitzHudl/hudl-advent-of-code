"""Advent of Code 2025 - Day 4."""

import logging
import time

import networkx as nx


logger = logging.getLogger(__name__)


def create_nodes(grid: list[str]) -> nx.Graph:
    """Create the paper graph."""
    g = nx.Graph()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "@":
                g.add_node((i, j))

    return g


def create_edges(g: nx.Graph) -> None:
    """Make connections."""
    for node in g:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                check_node = (node[0] + i, node[1] + j)
                if (
                    node != check_node
                    and check_node[0] >= 0
                    and check_node[1] >= 0
                    and check_node in g.nodes
                ):
                    g.add_edge(node, check_node)


def part_1(g: nx.Graph) -> int:
    """Calculate how many rolls of paper have fewer than four neighbors."""
    num_movable = 0
    for node in g:
        if len(list(g.neighbors(node))) < 4:  # noqa: PLR2004
            num_movable += 1
    return num_movable


def part_2(g: nx.Graph) -> int:
    """Remove rolls of paper until no rolls can be removed."""
    num_removed = 0
    while True:
        iter_removed = 0
        g_copy = g.copy()
        for node in g:
            if len(list(g.neighbors(node))) < 4:  # noqa: PLR2004
                num_removed += 1
                iter_removed += 1
                g_copy.remove_node(node)
        # Stop once we cycle through and remove no rolls.
        if iter_removed == 0:
            break
        g = g_copy
    return num_removed


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

    # Part 1:
    start_time = time.perf_counter()
    g = create_nodes(lines)
    create_edges(g)
    part1_result = part_1(g)
    part1_time = time.perf_counter() - start_time
    logger.info("Part 1: %s (%.4fs)", part1_result, part1_time)

    # Part 2:
    start_time = time.perf_counter()
    g = create_nodes(lines)
    create_edges(g)
    part2_result = part_2(g)
    part2_time = time.perf_counter() - start_time
    logger.info("Part 2: %s (%.4fs)", part2_result, part2_time)

    return part1_result, part2_result
