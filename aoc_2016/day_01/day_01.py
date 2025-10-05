from enum import Enum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def rotate(self, rotation: str):
        if rotation == "L":
            return Direction((self.value - 1) % 4 or 4)
        elif rotation == "R":
            return Direction((self.value + 1) % 4 or 4)
        return None

    def advance(self, steps: int):
        if self == Direction.UP:
            return 0, steps
        elif self == Direction.DOWN:
            return 0, -steps
        elif self == Direction.LEFT:
            return -steps, 0
        elif self == Direction.RIGHT:
            return steps, 0

    def advance_one_step(self):
        if self == Direction.UP:
            return 0, 1
        elif self == Direction.DOWN:
            return 0, -1
        elif self == Direction.LEFT:
            return -1, 0
        elif self == Direction.RIGHT:
            return 1, 0


class Rotation(Enum):
    LEFT = "L"
    RIGHT = "R"


def part_one(instructions: list[tuple[Rotation, int]]) -> int:
    y, x = 0, 0
    direction = Direction.UP

    for rotation, steps in instructions:
        direction = direction.rotate(rotation.value)
        delta_x, delta_y = direction.advance(steps)
        y, x = y + delta_y, x + delta_x
    return y + x


def part_two(instructions: list[tuple[Rotation, int]]) -> int:
    y, x = 0, 0
    direction = Direction.UP
    history = {(y, x)}

    for rotation, steps in instructions:
        direction = direction.rotate(rotation.value)
        delta_x, delta_y = direction.advance_one_step()
        for _ in range(steps):
            y, x = y + delta_y, x + delta_x
            if (y, x) in history:
                return y + x
            history.add((y, x))
    raise ValueError("No solution found")


def parse_input(filename: str) -> list[tuple[Rotation, int]]:
    with open(filename) as f:
        raw_instructions = f.read().split(", ")
        return [(Rotation(line[0]), int(line[1:])) for line in raw_instructions]


def main():
    instructions = parse_input("input_part_1.txt")
    result_1 = part_one(instructions)
    print(f"Result part 1: {result_1}")

    instructions = parse_input("input_part_2.txt")
    result_2 = part_two(instructions)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
