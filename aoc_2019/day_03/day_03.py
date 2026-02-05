from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def manhattan_distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def part_one(path_a: list[Point], path_b: list[Point]) -> int:
    origin = Point(0, 0)
    intersections = (set(path_a) & set(path_b)) ^ {origin}
    return min(origin.manhattan_distance(p) for p in intersections)


def part_two(path_a: list[Point], path_b: list[Point]) -> int:
    intersections = (set(path_a) & set(path_b)) ^ {Point(0, 0)}
    min_distance = float("inf")
    for point in intersections:
        distance = path_a.index(point) + path_b.index(point)
        min_distance = min(min_distance, distance)
    return min_distance


def get_path_from_line(line: str) -> list[Point]:
    origin = Point(0, 0)
    last_point = origin
    points = [origin]

    for move in line.split(","):
        direction = move[0]
        distance = int(move[1:])
        deltas = {
            "U": (0, -1),
            "D": (0, 1),
            "L": (-1, 0),
            "R": (1, 0),
        }
        delta_x, delta_y = deltas[direction]
        for _ in range(distance):
            new_point = Point(last_point.x + delta_x, last_point.y + delta_y)
            points.append(new_point)
            last_point = new_point
    return points


def parse_input(filename: str) -> tuple[list[Point], list[Point]]:
    with open(filename) as f:
        lines = f.readlines()
        return get_path_from_line(lines[0]), get_path_from_line(lines[1])


def main():
    path_a, path_b = parse_input("input_part_1.txt")
    result_1 = part_one(path_a, path_b)
    print(f"Result part 1: {result_1}")

    path_a, path_b = parse_input("input_part_2.txt")
    result_2 = part_two(path_a, path_b)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
