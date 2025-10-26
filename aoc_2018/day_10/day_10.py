import re
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    x_velocity: int
    y_velocity: int

    def tick(self):
        self.x += self.x_velocity
        self.y += self.y_velocity


def render(coords: list[tuple[int, int]]) -> str:
    xs = [x for x, _ in coords]
    ys = [y for _, y in coords]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    grid = [["."] * (width + 2) for _ in range(height + 2)]
    points = set(coords)

    for x, y in points:
        grid_x_index = x - min_x
        grid_y_index = y - min_y
        if 0 <= grid_y_index < len(grid) and 0 <= grid_x_index < len(grid[0]):
            grid[grid_y_index][grid_x_index] = "#"

    return "\n" + "\n".join("".join(row) for row in grid)


def is_letter(points: list[Point]) -> bool:
    points_set = {(p.x, p.y) for p in points}
    for x, y in points_set:
        # Only start counting if there's no predecessor (avoid re-counting runs)
        if (x, y - 1) not in points_set:
            run = 1
            while (x, y + run) in points_set:
                run += 1
                if run >= 8:
                    return True
    return False


def part_one_and_two(points: list[Point]) -> tuple[str, int]:
    points = sorted(points, key=lambda p: p.y)
    found_at = None
    for second in range(14_000):
        for point in points:
            point.tick()
        if is_letter(points):
            found_at = second
            break

    return render([(p.x, p.y) for p in points]), found_at


def parse_input(filename: str) -> list[Point]:
    pattern = re.compile(
        r"\s*position=<\s*(-?\d+),\s*(-?\d+)>\s+velocity=<\s*(-?\d+),\s*(-?\d+)>\s*"
    )
    points = []
    with open(filename) as f:
        for line in f.readlines():
            if result := pattern.match(line):
                point = Point(*map(int, result.groups()))
                points.append(point)
    return points


def main():
    points = parse_input("input_part_1.txt")
    result_1, result_2 = part_one_and_two(points)
    print(f"Result part 1: {result_1}")
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
