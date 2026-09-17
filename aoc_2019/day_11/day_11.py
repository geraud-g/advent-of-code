from collections import defaultdict
from dataclasses import dataclass
from enum import Enum

from lib.intcode import Process


@dataclass(frozen=True)
class Point:
    x: int
    y: int


BLACK: int = 0
WHITE: int = 1
TURN_LEFT: int = 0
TURN_RIGHT: int = 1


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def rotate(self, direction: int) -> "Direction":
        if direction == TURN_LEFT:
            return Direction((self.value - 1) % 4)
        else:
            return Direction((self.value + 1) % 4)

    def get_new_position(self, position: Point) -> Point:
        match self:
            case Direction.UP:
                return Point(position.x, position.y - 1)
            case Direction.RIGHT:
                return Point(position.x + 1, position.y)
            case Direction.DOWN:
                return Point(position.x, position.y + 1)
            case Direction.LEFT:
                return Point(position.x - 1, position.y)


def _get_painted_tiles(
    intcode: list[int], painted: dict[Point, int]
) -> dict[Point, int]:
    painted = painted.copy()
    robot_direction = Direction.UP
    robot_position = Point(0, 0)
    program = Process(intcode.copy(), [])
    while not program.exited:
        program.add_input(painted[robot_position])
        program.run_until_output()
        if program.exited:
            break
        color = program.get_output()
        painted[robot_position] = color

        program.run_until_output()
        rotation = program.get_output()
        robot_direction = robot_direction.rotate(rotation)
        robot_position = robot_direction.get_new_position(robot_position)
    return painted


def part_one(intcode: list[int]) -> int:
    painted = defaultdict(int)
    painted = _get_painted_tiles(intcode, painted)
    return len(painted)


def part_two(intcode: list[int]) -> str:
    painted = defaultdict(int)
    painted[Point(0, 0)] = WHITE
    painted = _get_painted_tiles(intcode, painted)

    output = "\n"
    max_y = max(t.y for t in painted)
    max_x = max(t.x for t in painted)
    for y in range(0, max_y + 1):
        line = ""
        for x in range(0, max_x + 1):
            if painted[Point(x=x, y=y)] == BLACK:
                line += "."
            else:
                line += "█"
        output += f"{line}\n"
    return output[:-1]


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(c) for c in f.readline().split(",")]


def main():
    intcode = parse_input("input_part_1.txt")
    result_1 = part_one(intcode)
    print(f"Result part 1: {result_1}")

    intcode = parse_input("input_part_2.txt")
    result_2 = part_two(intcode)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
