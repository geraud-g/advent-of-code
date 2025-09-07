from typing import TypeAlias

Keypad: TypeAlias = list[list[str | None]]


KEYPAD_1: Keypad = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
]

KEYPAD_2: Keypad = [
    [None, None, "1", None, None],
    [None, "2", "3", "4", None],
    ["5", "6", "7", "8", "9"],
    [None, "A", "B", "C", None],
    [None, None, "D", None, None],
]


DIRECTIONS: dict[str, (int, int)] = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


def get_value(keypad: Keypad, y: int, x: int) -> str | None:
    if 0 <= y < len(keypad) and 0 <= x < len(keypad[0]):
        return keypad[y][x]
    return None


def get_code(keypad: Keypad, instructions: list[str], y: int, x: int) -> str:
    code = ""
    for line in instructions:
        for char in line.strip():
            dy, dx = DIRECTIONS[char]
            new_y = y + dy
            new_x = x + dx
            if get_value(keypad, new_y, new_x):
                y, x = new_y, new_x
        code += str(keypad[y][x])
    return code


def part_one(instructions: list[str]) -> str:
    return get_code(KEYPAD_1, instructions, 1, 1)


def part_two(instructions: list[str]) -> str:
    return get_code(KEYPAD_2, instructions, 2, 0)


def main():
    with open("input_part_1.txt") as f:
        instructions = f.readlines()
        result_1 = part_one(instructions)
        print(f"Result part 1: {result_1}")

    with open("input_part_2.txt") as f:
        instructions = f.readlines()
        result_2 = part_two(instructions)
        print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
