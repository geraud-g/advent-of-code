from collections import deque
from dataclasses import dataclass
from typing import Any, Generator


@dataclass(frozen=True)
class Node:
    x: int
    y: int


def get_neighbours(
    node: Node, favourite_number: int
) -> Generator[Node, Any, None]:  # TODO : iter ?
    for delta_x, delta_y in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = node.x + delta_x
        new_y = node.y + delta_y
        if new_x < 0 or new_y < 0:
            continue
        value = new_x * new_x + 3 * new_x + 2 * new_x * new_y + new_y + new_y * new_y
        value += favourite_number
        if value.bit_count() % 2 == 0:
            yield Node(x=new_x, y=new_y)


def reconstruct_path(
    came_from: dict[Node, Node | None], start: Node, goal: Node
) -> list[Node]:
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def bfs(start: Node, goal: Node, favourite_number: int) -> list[Node]:
    frontier = deque()
    frontier.append(start)
    came_from = dict()
    came_from[start] = None

    while frontier:
        current: Node = frontier.pop()
        for neighbour in get_neighbours(current, favourite_number):
            if neighbour not in came_from:
                frontier.append(neighbour)
                came_from[neighbour] = current
                if neighbour == goal:
                    return reconstruct_path(came_from, start, goal)
    raise ValueError(f"No path found from {start} to {goal}")


def bfs_max_range(start: Node, favourite_number: int) -> int:
    frontier = deque()
    frontier.append(start)
    came_from = dict()
    came_from[start] = None
    cost_so_far = dict()
    cost_so_far[start] = 0

    while frontier:
        current: Node = frontier.pop()
        for neighbour in get_neighbours(current, favourite_number):
            current_cost = cost_so_far[current]
            neighbour_cost = current_cost + 1
            if current_cost <= 50 and neighbour not in came_from:
                came_from[neighbour] = current
                cost_so_far[neighbour] = neighbour_cost
                frontier.append(neighbour)
    return len(cost_so_far)


def part_one(favourite_number: int) -> int:
    path = bfs(Node(x=1, y=1), Node(x=31, y=39), favourite_number)
    return len(path) - 1  # Exclude the starting node


def part_two(favourite_number: int) -> int:
    count = bfs_max_range(Node(x=1, y=1), favourite_number)
    return count


def parse_input(file_path: str) -> int:
    with open(file_path) as f:
        return int(f.readline().strip())


def main():
    favourite_number = parse_input("input_part_1.txt")
    result_1 = part_one(favourite_number)
    print(f"Result part 1: {result_1}")

    favourite_number = parse_input("input_part_2.txt")
    result_2 = part_two(favourite_number)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
