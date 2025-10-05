from collections import deque
from dataclasses import dataclass
from itertools import permutations
from typing import TypeAlias

Grid: TypeAlias = list[list[bool]]


@dataclass(frozen=True)
class Node:
    x: int
    y: int


def get_neighbours(grid: Grid, node: Node):
    if not grid[node.y - 1][node.x]:
        yield Node(x=node.x, y=node.y - 1)
    if not grid[node.y + 1][node.x]:
        yield Node(x=node.x, y=node.y + 1)
    if not grid[node.y][node.x + 1]:
        yield Node(x=node.x + 1, y=node.y)
    if not grid[node.y][node.x - 1]:
        yield Node(x=node.x - 1, y=node.y)


def get_path_length(came_from: dict[Node, Node | None], start: Node, goal: Node) -> int:
    length = 0
    current = goal
    while current != start:
        length += 1
        current = came_from[current]
    return length


def bfs(grid: Grid, start: Node, goal: Node) -> int:
    frontier = deque()
    frontier.append(start)
    came_from = dict()
    came_from[start] = None

    while frontier:
        current: Node = frontier.popleft()
        for neighbour in get_neighbours(grid, current):
            if neighbour not in came_from:
                frontier.append(neighbour)
                came_from[neighbour] = current
                if neighbour == goal:
                    return get_path_length(came_from, start, goal)
    raise ValueError(f"No path found from {start} to {goal}")


def get_min_path_len(
    grid: Grid, objectives: list[Node], start: Node, part_two: bool
) -> int:
    path_lengths = {o: dict() for o in objectives}

    # Compute all path between objectives
    for idx, objective_a in enumerate(objectives):
        for objective_b in objectives[idx + 1 :]:
            path_len = bfs(grid, objective_a, objective_b)
            path_lengths[objective_a][objective_b] = path_len
            path_lengths[objective_b][objective_a] = path_len

    # Find the combination with the smallest length
    min_path_length = float("inf")
    objectives = [o for o in objectives if o != start]
    for p in permutations(objectives):
        all_objectives = [start] + list(p)
        if part_two:
            all_objectives += [start]
        path_length = 0
        for i in range(len(all_objectives) - 1):
            path_length += path_lengths[all_objectives[i]][all_objectives[i + 1]]
        min_path_length = min(min_path_length, path_length)
    return min_path_length


def parse_input(file_path: str) -> tuple[Grid, list[Node], Node]:
    grid = list()
    objectives = list()
    start = None
    with open(file_path) as f:
        lines = f.readlines()
    for y, line in enumerate(lines):
        new_line = list()
        for x, c in enumerate(line):
            if c == "0":
                start = Node(x=x, y=y)
                objectives.append(Node(x=x, y=y))
            elif c == "#":
                new_line.append(True)
            else:
                new_line.append(False)
                if c.isdigit():
                    objectives.append(Node(x=x, y=y))
        if new_line:
            grid.append(new_line)
    if start is None:
        raise Exception("Could not find start")
    return grid, objectives, start


def main():
    grid, objectives, start = parse_input("input_part_1.txt")
    result_1 = get_min_path_len(grid, objectives, start, False)
    print(f"Result part 1: {result_1}")

    grid, objectives, start = parse_input("input_part_1.txt")
    result_2 = get_min_path_len(grid, objectives, start, True)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
