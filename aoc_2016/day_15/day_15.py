import re
from dataclasses import dataclass


REGEX_DISC = re.compile(
    r"Disc #(\d) has (\d+) positions; at time=0, it is at position (\d+)."
)


@dataclass
class Disc:
    disc_id: int
    positions: int
    current_position: int


def solve_day(discs: list[Disc]) -> int:
    for disc in discs:
        # Update disc position to the time it would be reached
        disc.current_position = (disc.current_position + disc.disc_id) % disc.positions

    for delay in range(1_000_000_000):
        if all(disc.current_position == 0 for disc in discs):
            return delay
        for disc in discs:
            disc.current_position = (disc.current_position + 1) % disc.positions
    raise ValueError("No solution found")


def parse_input(file_path: str) -> list[Disc]:
    with open(file_path) as f:
        lines = f.readlines()
    discs = []
    for line in lines:
        match = REGEX_DISC.match(line.strip())
        if match:
            disc_id, positions, current_position = match.groups()
            discs.append(
                Disc(
                    disc_id=int(disc_id),
                    positions=int(positions),
                    current_position=int(current_position),
                )
            )
    return discs


def main():
    discs = parse_input("input_part_1.txt")
    result_1 = solve_day(discs)
    print(f"Result part 1: {result_1}")

    discs = parse_input("input_part_2.txt")
    discs.append(Disc(disc_id=len(discs) + 1, positions=11, current_position=0))
    result_2 = solve_day(discs)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
