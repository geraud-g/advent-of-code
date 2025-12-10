import re
from collections import deque
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any


@dataclass
class Machine:
    light: int
    buttons: list[int]
    jolts: list[int]


def get_possible_states(light: int, buttons: list[int]) -> Generator[int, Any, None]:
    for button in buttons:
        yield light ^ button


def get_fewer_presses(machine: Machine) -> int:
    queue = deque([(0, 0)])
    visited = {0}

    while queue:
        state, presses = queue.popleft()
        if state == machine.light:
            return presses
        for new_state in get_possible_states(state, machine.buttons):
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, presses + 1))
    return -1


def part_one(machines: list[Machine]) -> int:
    return sum(get_fewer_presses(m) for m in machines)


def part_two(machine: Machine) -> int:
    pass


def parse_input(filename: str) -> list[Machine]:
    machines = []
    with open(filename) as f:
        for line in f.readlines():
            # Light
            light_str = re.search(r"\[([.#]+)\]", line).group(1)
            light = int("".join("1" if c == "#" else "0" for c in light_str)[::-1], 2)

            # Buttons
            buttons = []
            for match in re.findall(r"\(([0-9,]+)\)", line):
                indices = [int(x) for x in match.split(",")]
                mask = sum(1 << idx for idx in indices)
                buttons.append(mask)

            # Jolts
            jolt_str = re.search(r"\{([0-9,]+)\}", line).group(1)
            jolts = [int(x) for x in jolt_str.split(",")]

            machines.append(Machine(light=light, buttons=buttons, jolts=jolts))

    return machines


def main():
    machines = parse_input("input_part_1.txt")
    result_1 = part_one(machines)
    print(f"Result part 1: {result_1}")

    machines = parse_input("input_part_2.txt")
    result_2 = part_two(machines)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
