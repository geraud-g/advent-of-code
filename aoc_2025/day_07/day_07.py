from functools import cache
from typing import TypeAlias

Grid: TypeAlias = tuple[tuple[bool, ...], ...]
EMPTY_SPACE: bool = False
SPLITTER: bool = True


def part_one(diagram: Grid, start: int) -> int:
    split_count = 0
    current_tachyons_x = {start}

    for line in diagram:
        for x, val in enumerate(line):
            if val == SPLITTER and x in current_tachyons_x:
                current_tachyons_x.add(x - 1)
                current_tachyons_x.add(x + 1)
                current_tachyons_x.remove(x)
                split_count += 1
    return split_count


@cache
def compute_path(diagram: Grid, point_y: int, point_x: int) -> int:
    if point_y == len(diagram):
        return 0
    timelines = 0
    if diagram[point_y][point_x] == SPLITTER:
        timelines += 1
        timelines += compute_path(diagram, point_y + 1, point_x - 1)
        timelines += compute_path(diagram, point_y + 1, point_x + 1)
    else:
        timelines += compute_path(diagram, point_y + 1, point_x)

    return timelines


def part_two(diagram: Grid, start: int) -> int:
    return compute_path(diagram, 0, start) + 1


def parse_input(filename: str) -> tuple[Grid, int]:
    with open(filename) as f:
        lines = [line.strip() for line in f]

    start = lines[0].index("S")
    diagram = tuple(tuple(char == "^" for char in line) for line in lines)

    return diagram, start


def main():
    diagram, start = parse_input("input_part_1.txt")
    result_1 = part_one(diagram, start)
    print(f"Result part 1: {result_1}")

    diagram, start = parse_input("input_part_2.txt")
    result_2 = part_two(diagram, start)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
