from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def manhattan_distance(y_a, x_a, y_b, x_b):
    return abs(y_a - y_b) + abs(x_a - x_b)


def get_closest_point_id(points: list[Point], y: int, x: int) -> int | None:
    min_distance = float("inf")
    closest_point = None
    for idx, point in enumerate(points):
        distance = manhattan_distance(point.y, point.x, y, x)
        if distance < min_distance:
            min_distance = distance
            closest_point = idx
        elif distance == min_distance:
            closest_point = None
    return closest_point


def part_one(points: list[Point]) -> int:
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    distances = defaultdict(int)
    to_exclude = {None}

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            closest_point = get_closest_point_id(points, y, x)
            distances[closest_point] += 1
            if y == max_y or x == max_x or y == min_y or x == min_x:
                to_exclude.add(closest_point)

    return max(value for key, value in distances.items() if key not in to_exclude)


def is_within_10k_reach(points: list[Point], y: int, x: int) -> bool:
    distance_sum = 0
    for point in points:
        distance = manhattan_distance(point.y, point.x, y, x)
        distance_sum += distance
        if distance_sum >= 10_000:
            return False
    return True


def part_two(points: list[Point]) -> int:
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    region_size = 0

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if is_within_10k_reach(points, y, x):
                region_size += 1
    return region_size


def parse_input(filename: str) -> list[Point]:
    points = []
    with open(filename) as f:
        for line in f.readlines():
            points.append(Point(*map(int, line.split(","))))
    return points


def main():
    points = parse_input("input_part_1.txt")
    result_1 = part_one(points)
    print(f"Result part 1: {result_1}")

    points = parse_input("input_part_2.txt")
    result_2 = part_two(points)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
