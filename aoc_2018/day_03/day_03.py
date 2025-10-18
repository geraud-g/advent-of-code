import re
from dataclasses import dataclass


@dataclass
class Claim:
    id: int
    y: int
    x: int
    width: int
    height: int

    def intersects(self, other: "Claim") -> bool:
        return not (
            self.x + self.width <= other.x
            or other.x + other.width <= self.x
            or self.y + self.height <= other.y
            or other.y + other.height <= self.y
        )


def part_one(claims: list[Claim]) -> int:
    max_y = max([c.y + c.height for c in claims])
    max_x = max([c.x + c.width for c in claims])
    grid = [[0 for _ in range(max_x)] for _ in range(max_y)]
    for claim in claims:
        for y in range(claim.y, claim.y + claim.height):
            for x in range(claim.x, claim.x + claim.width):
                grid[y][x] += 1
    counter = 0
    for row in grid:
        counter += sum(1 for c in row if c >= 2)
    return counter


def part_two(claims: list[Claim]) -> int:
    for claim in claims:
        if all(not claim.intersects(c) for c in claims if c.id != claim.id):
            return claim.id
    raise ValueError("No solution found for part 2")


def parse_input(filename: str) -> list[Claim]:
    re_claim = re.compile(r"#(\d+)\s+@ (\d+),(\d+): (\d+)x(\d+)")
    claims = []
    with open(filename) as f:
        for line in f.readlines():
            if match := re_claim.match(line):
                claims.append(
                    Claim(
                        id=int(match.group(1)),
                        x=int(match.group(2)),
                        y=int(match.group(3)),
                        width=int(match.group(4)),
                        height=int(match.group(5)),
                    )
                )
    return claims


def main():
    claims = parse_input("input_part_1.txt")
    result_1 = part_one(claims)
    print(f"Result part 1: {result_1}")

    claims = parse_input("input_part_2.txt")
    result_2 = part_two(claims)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
