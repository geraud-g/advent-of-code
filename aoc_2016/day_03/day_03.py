from typing import TypeAlias

Triangle: TypeAlias = tuple[int, int, int]


def _is_valid_triangle(triangle: Triangle) -> bool:
    a, b, c = triangle
    return a + b > c and a + c > b and b + c > a


def part_one(triangles: list[Triangle]) -> int:
    return sum(1 for triangle in triangles if _is_valid_triangle(triangle))


def part_two(triangles: list[Triangle]) -> int:
    valid_triangles = 0
    for y in range(0, len(triangles), 3):
        for x in range(0, 3):
            triangle = (
                triangles[y][x],
                triangles[y + 1][x],
                triangles[y + 2][x],
            )
            valid_triangles += _is_valid_triangle(triangle)
    return valid_triangles


def main():
    with open("input_part_1.txt") as f:
        triangles = [s.split() for s in f.readlines()]
        triangles = [(int(x[0]), int(x[1]), int(x[2])) for x in triangles]
        result_1 = part_one(triangles)
        print(f"Result part 1: {result_1}")

    with open("input_part_2.txt") as f:
        triangles = [s.split() for s in f.readlines()]
        triangles = [(int(x[0]), int(x[1]), int(x[2])) for x in triangles]
        result_2 = part_two(triangles)
        print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
