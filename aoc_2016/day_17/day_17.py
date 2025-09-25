from collections import deque
from dataclasses import dataclass
from hashlib import md5


@dataclass(frozen=True)
class Node:
    x: int
    y: int


def get_neighbours(node: Node, history: str):
    digest = md5(history.encode()).hexdigest().lower()
    # print(f"D: digest={digest}, history={history}")
    # print(f"  {digest[0]=}, {digest[1]=}, {digest[2]=}, {digest[3]=}")
    if digest[0] in "bcdef" and node.y > 0:  # UP
        yield history + "U", Node(x=node.x, y=node.y - 1)
    if digest[1] in "bcdef" and node.y < 3:  # DOWN
        yield history + "D", Node(x=node.x, y=node.y + 1)
    if digest[2] in "bcdef" and node.x > 0:  # LEFT
        yield history + "L", Node(x=node.x - 1, y=node.y)
    if digest[3] in "bcdef" and node.x < 3:  # RIGHT
        yield history + "R", Node(x=node.x + 1, y=node.y)


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


def bfs(start: Node, passcode: str) -> str:
    frontier = deque()
    frontier.append((passcode, start))
    end = Node(x=3, y=3)

    while frontier:
        history, current = frontier.popleft()
        for neighbour_history, neighbour in get_neighbours(current, history):
            frontier.append((neighbour_history, neighbour))
            if neighbour == end:
                return neighbour_history
    raise ValueError(f"No path found from {start} to {end}")


def bfs_all_path(start: Node, passcode: str) -> int:
    frontier = deque()
    frontier.append((passcode, start))
    end = Node(x=3, y=3)
    longest_path_length = 0

    while frontier:
        history, current = frontier.popleft()

        for neighbour_history, neighbour in get_neighbours(current, history):
            if neighbour == end:
                path_length = len(neighbour_history)
                if path_length > longest_path_length:
                    longest_path_length = path_length
            else:
                frontier.append((neighbour_history, neighbour))
    return longest_path_length - len(passcode)


def part_one(passcode: str) -> str:
    path = bfs(Node(x=0, y=0), passcode)
    return path[len(passcode) :]


def part_two(passcode: str) -> int:
    return bfs_all_path(Node(x=0, y=0), passcode)


def parse_input(file_path: str) -> str:
    with open(file_path) as f:
        return f.readline().strip()


def main():
    passcode = parse_input("input_part_1.txt")
    result_1 = part_one(passcode)
    print(f"Result part 1: {result_1}")

    passcode = parse_input("input_part_2.txt")
    result_2 = part_two(passcode)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
