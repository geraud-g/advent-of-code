from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def is_accessible(rolls: list[list[int]], roll: Point) -> bool:
    delta = [-1, 0, 1]
    total = 0
    for delta_x in delta:
        for delta_y in delta:
            if delta_x == 0 and delta_y == 0:
                continue
            candidate_x, candidate_y = roll.x + delta_x, roll.y + delta_y
            if 0 <= candidate_x < len(rolls[0]) and 0 <= candidate_y < len(rolls):
                total += rolls[candidate_y][candidate_x]
    return total < 4


def get_accessible_rolls(rolls: list[list[int]]) -> list[Point]:
    accessible_rolls = []
    for y, line in enumerate(rolls):
        for x, roll_value in enumerate(line):
            if roll_value == 1:
                roll = Point(x=x, y=y)
                if is_accessible(rolls, roll):
                    accessible_rolls.append(roll)
    return accessible_rolls


def part_one(rolls: list[list[int]]) -> int:
    return len(get_accessible_rolls(rolls))


def part_two(rolls: list[list[int]]) -> int:
    removed_rolls = 0
    while accessible_rolls := get_accessible_rolls(rolls):
        removed_rolls += len(accessible_rolls)
        for accessible_roll in accessible_rolls:
            rolls[accessible_roll.y][accessible_roll.x] = 0
    return removed_rolls


def parse_input(filename: str) -> list[list[int]]:
    rolls = []
    with open(filename) as f:
        for line in f.readlines():
            roll_line = [1 if c == "@" else 0 for c in line.strip()]
            rolls.append(roll_line)
    return rolls


def main():
    rolls = parse_input("input_part_1.txt")
    result_1 = part_one(rolls)
    print(f"Result part 1: {result_1}")

    rolls = parse_input("input_part_2.txt")
    result_2 = part_two(rolls)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
