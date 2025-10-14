import re
from collections import deque
from dataclasses import dataclass
from itertools import chain


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int
    available: int

    def copy(self):
        return Node(self.x, self.y, self.size, self.used, self.available)

    def __hash__(self):
        return hash((self.x, self.y, self.size, self.used))


@dataclass
class Grid:
    nodes: list[list[Node]]
    data_location: Point
    empty_location: Point

    def signature(self: "Grid") -> tuple[int, int, int, int]:
        return (
            self.data_location.x,
            self.data_location.y,
            self.empty_location.x,
            self.empty_location.y,
        )

    def __hash__(self) -> int:
        return hash(self.signature())

    def __eq__(self, other: "Grid") -> bool:
        return self.signature() == other.signature()

    def get_new_state(self, from_point: Point, to_point: Point):
        new_state = self.copy()
        from_node = new_state.nodes[from_point.y][from_point.x]
        to_node = new_state.nodes[to_point.y][to_point.x]

        # move data: from_node -> to_node
        moved = from_node.used
        # sanity
        assert moved <= to_node.available

        # apply transfer
        to_node.used += moved
        to_node.available -= moved
        from_node.used = 0
        from_node.available = from_node.size

        # data location moves with the data source
        if self.data_location == from_point:
            new_state.data_location = to_point

        # EMPTY LOCATION: since data moved into the empty (dest == old empty),
        # the empty relocates to the source cell.
        if self.empty_location == to_point:
            new_state.empty_location = from_point

        return new_state

    def copy(self) -> "Grid":
        new_grid = [[node.copy() for node in line] for line in self.nodes]
        return Grid(
            nodes=new_grid,
            data_location=Point(self.data_location.x, self.data_location.y),
            empty_location=Point(self.empty_location.x, self.empty_location.y),
        )


def get_neighbors(grid: Grid, y: int, x: int):
    if y > 0:
        yield Point(y=y - 1, x=x)
    if x > 0:
        yield Point(y=y, x=x - 1)
    if x < len(grid.nodes[y]) - 1:
        yield Point(y=y, x=x + 1)
    if y < len(grid.nodes) - 1:
        yield Point(y=y + 1, x=x)


def is_valid_move(from_node: Node, to_node: Node) -> bool:
    return 0 < from_node.used <= to_node.available


def bfs(start: Grid, target: Point) -> int:
    frontier = deque([start])
    came_from = {start: None}
    dist = {start: 0}

    while frontier:
        current_state: Grid = frontier.popleft()
        if current_state.empty_location == target:
            return dist[current_state]

        ey, ex = current_state.empty_location.y, current_state.empty_location.x
        empty_node = current_state.nodes[ey][ex]

        for neighbour in get_neighbors(current_state, ey, ex):
            neighbour_node = current_state.nodes[neighbour.y][neighbour.x]

            # MOVE DATA neighbour -> empty
            if is_valid_move(neighbour_node, empty_node):
                new_state = current_state.get_new_state(
                    neighbour, current_state.empty_location
                )

                if new_state not in came_from:
                    frontier.append(new_state)
                    # noinspection PyTypeChecker
                    came_from[new_state] = current_state
                    dist[new_state] = dist[current_state] + 1

    raise ValueError(f"No path found from {start}")


def part_two(grid: Grid) -> int:
    goal = Point(y=grid.data_location.y, x=grid.data_location.x - 1)
    path = bfs(grid, goal)
    total_len = path + 5 * goal.x + 1
    return total_len


def to_grid(nodes: list[Node]) -> Grid:
    max_x = max(n.x for n in nodes)
    max_y = max(n.y for n in nodes)
    # noinspection PyTypeChecker
    grid: list[list[Node]] = [
        [None for _ in range(max_x + 1)] for _ in range(max_y + 1)
    ]
    for n in nodes:
        grid[n.y][n.x] = n

    empty_node = None
    for line in grid:
        for node in line:
            if node.used == 0:
                empty_node = Point(x=node.x, y=node.y)
                break

    if empty_node is None:
        raise ValueError("Empty node not found")
    return Grid(
        nodes=grid,
        data_location=Point(x=len(grid[0]) - 1, y=0),
        empty_location=empty_node,
    )


def parse_input(file_path: str) -> Grid:
    nodes = []
    re_node = re.compile(r"node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)")
    with open(file_path) as f:
        for line in f.readlines()[2:]:
            if match := re_node.search(line.strip()):
                nodes.append(
                    Node(
                        int(match.group(1)),
                        int(match.group(2)),
                        int(match.group(3)),
                        int(match.group(4)),
                        int(match.group(5)),
                    )
                )
    return to_grid(nodes)


def part_one(grid: Grid) -> int:
    viable_pairs = 0
    nodes = list(chain.from_iterable(grid.nodes))
    for node in nodes:
        if node.used == 0:
            continue
        for node_b in nodes:
            if node.y == node_b.y and node.x == node_b.x:
                continue
            if node.used <= node_b.available:
                viable_pairs += 1
    return viable_pairs


def main():
    grid = parse_input("input_part_1.txt")
    result_1 = part_one(grid)
    print(f"Result part 1: {result_1}")

    grid = parse_input("input_part_2.txt")
    result_2 = part_two(grid)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
