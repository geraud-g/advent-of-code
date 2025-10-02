import re
from collections import deque
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"


@dataclass
class Operation:
    def process(self, password: deque[str]) -> None:
        raise NotImplementedError()

    def process_reverse(self, password: deque[str]) -> None:
        raise NotImplementedError()


@dataclass
class SwapPosition(Operation):
    x: int
    y: int

    def process(self, password: deque[str]) -> None:
        password[self.x], password[self.y] = password[self.y], password[self.x]

    def process_reverse(self, password: deque[str]) -> None:
        self.process(password)


@dataclass
class SwapLetter(Operation):
    x: str
    y: str

    def process(self, password: deque[str]) -> None:
        x_idx = password.index(self.x)
        y_idx = password.index(self.y)
        password[x_idx], password[y_idx] = password[y_idx], password[x_idx]

    def process_reverse(self, password: deque[str]) -> None:
        self.process(password)


@dataclass
class RotateDirection(Operation):
    direction: Direction
    steps: int

    def process(self, password: deque[str]) -> None:
        match self.direction:
            case Direction.LEFT:
                password.rotate(-self.steps)
            case Direction.RIGHT:
                password.rotate(self.steps)

    def process_reverse(self, password: deque[str]) -> None:
        match self.direction:
            case Direction.LEFT:
                password.rotate(self.steps)
            case Direction.RIGHT:
                password.rotate(-self.steps)


@dataclass
class RotateBasedOn(Operation):
    letter: str

    def process(self, password: deque[str]) -> None:
        initial_idx = password.index(self.letter)
        rotate_nbr = initial_idx + 1
        if initial_idx >= 4:
            rotate_nbr += 1
        password.rotate(rotate_nbr)

    def process_reverse(self, password: deque[str]) -> None:
        for i in range(len(password) + 5):
            current_password = password.copy()
            current_password.rotate(-i)
            self.process(current_password)
            if current_password == password:
                password.rotate(-i)
                return
        raise ValueError(f"Cannot find inverse for {self.letter}")


@dataclass
class Reverse(Operation):
    x: int
    y: int

    def process(self, password: deque[str]) -> None:
        buffer = []
        for i in range(self.x, self.y + 1):
            buffer.append(password[i])
        for i, n in enumerate(range(self.y, self.x - 1, -1)):
            password[n] = buffer[i]

    def process_reverse(self, password: deque[str]) -> None:
        self.process(password)


@dataclass
class Move(Operation):
    x: int
    y: int

    def process(self, password: deque[str]) -> None:
        value = password[self.x]
        password.remove(value)
        password.insert(self.y, value)

    def process_reverse(self, password: deque[str]) -> None:
        value = password[self.y]
        password.remove(value)
        password.insert(self.x, value)


def part_one(operations: list[Operation]) -> str:
    password: deque[str] = deque("abcdefgh")
    for operation in operations:
        operation.process(password)
    return "".join(password)


def part_two(operations: list[Operation]) -> str:
    password: deque[str] = deque("fbgdceah")
    for operation in reversed(operations):
        operation.process_reverse(password)
    return "".join(password)


def parse_input(file_path: str) -> list[Operation]:
    operations = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # swap position X with position Y
            if match := re.match(r"swap position (\d+) with position (\d+)", line):
                operations.append(
                    SwapPosition(int(match.group(1)), int(match.group(2)))
                )

            # swap letter X with letter Y
            elif match := re.match(r"swap letter (\w) with letter (\w)", line):
                operations.append(SwapLetter(match.group(1), match.group(2)))

            # rotate left/right X steps
            elif match := re.match(r"rotate (left|right) (\d+) steps?", line):
                operations.append(
                    RotateDirection(Direction(match.group(1)), int(match.group(2)))
                )

            # rotate based on position of letter X
            elif match := re.match(r"rotate based on position of letter (\w)", line):
                operations.append(RotateBasedOn(match.group(1)))

            # reverse positions X through Y
            elif match := re.match(r"reverse positions (\d+) through (\d+)", line):
                operations.append(Reverse(int(match.group(1)), int(match.group(2))))

            # move position X to position Y
            elif match := re.match(r"move position (\d+) to position (\d+)", line):
                operations.append(Move(int(match.group(1)), int(match.group(2))))

    return operations


def main():
    operations = parse_input("input_part_1.txt")
    result_1 = part_one(operations)
    print(f"Result part 1: {result_1}")

    operations = parse_input("input_part_2.txt")
    result_2 = part_two(operations)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
