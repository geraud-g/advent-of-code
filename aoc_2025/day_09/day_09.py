import itertools
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def get_rectangle_area(point_a: Point, point_b: Point) -> int:
    width = abs(point_a.x - point_b.x) + 1
    height = abs(point_a.y - point_b.y) + 1
    return width * height


def part_one(red_tiles: list[Point]) -> int:
    largest_area = -1
    for point_a, point_b in itertools.combinations(red_tiles, 2):
        largest_area = max(get_rectangle_area(point_a, point_b), largest_area)
    return largest_area


def part_two(red_tiles: list[Point]) -> int:
    pass


def parse_input(filename: str) -> list[Point]:
    points = []
    with open(filename) as f:
        for line in f.readlines():
            y, x = map(int, line.split(","))
            points.append(Point(x=x, y=y))
    return points


def main():
    data = parse_input("input_part_1.txt")
    result_1 = part_one(data)
    print(f"Result part 1: {result_1}")

    data = parse_input("input_part_2.txt")
    result_2 = part_two(data)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
