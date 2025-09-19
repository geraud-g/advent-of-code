import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

SCREEN_WIDTH: int = 50
SCREEN_HEIGHT: int = 6


class Instruction(ABC):
    @abstractmethod
    def apply(self, screen: list[list[bool]]) -> None:
        raise NotImplementedError()


@dataclass
class Rect(Instruction):
    width: int
    height: int

    def apply(self, screen: list[list[bool]]) -> None:
        for y in range(self.height):
            for x in range(self.width):
                screen[y][x] = True


@dataclass
class RotateRow(Instruction):
    y: int
    value: int

    def apply(self, screen: list[list[bool]]) -> None:
        screen[self.y] = screen[self.y][-self.value :] + screen[self.y][: -self.value]


@dataclass
class RotateColumn(Instruction):
    x: int
    value: int

    def apply(self, screen: list[list[bool]]) -> None:
        column = [screen[y][self.x] for y in range(SCREEN_HEIGHT)]
        column = column[-self.value :] + column[: -self.value]
        for y in range(SCREEN_HEIGHT):
            screen[y][self.x] = column[y]


def play_instructions(instructions: list[Instruction]) -> list[list[bool]]:
    screen = [[False] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
    for instruction in instructions:
        instruction.apply(screen)
    return screen


def part_one(instructions: list[Instruction]) -> int:
    screen = play_instructions(instructions)
    return sum(sum(row) for row in screen)


def part_two(instructions: list[Instruction]) -> str:
    screen = play_instructions(instructions)
    output = []
    for row in screen:
        output.append("".join("▓" if pixel else " " for pixel in row))
    return "\n".join(output)


def parse_input(file_path: str) -> list[Instruction]:
    rect_pattern = re.compile("rect (\d+)x(\d+)")
    rotate_col_pattern = re.compile("rotate column x=(\d+) by (\d+)")
    rotate_row_pattern = re.compile("rotate row y=(\d+) by (\d+)")
    with open(file_path) as f:
        lines = f.readlines()
    instructions = []
    for line in lines:
        if match := rect_pattern.match(line):
            instruction = Rect(width=int(match.group(1)), height=int(match.group(2)))
        elif match := rotate_col_pattern.match(line):
            instruction = RotateColumn(x=int(match.group(1)), value=int(match.group(2)))
        elif match := rotate_row_pattern.match(line):
            instruction = RotateRow(y=int(match.group(1)), value=int(match.group(2)))

        else:
            raise ValueError(f"Invalid instruction: {line}")
        instructions.append(instruction)
    return instructions


def main():
    instructions = parse_input("input_part_1.txt")
    result_1 = part_one(instructions)
    print(f"Result part 1: {result_1}")

    instructions = parse_input("input_part_2.txt")
    result_2 = part_two(instructions)
    print(f"Result part 2: \n{result_2}")


if __name__ == "__main__":
    main()
