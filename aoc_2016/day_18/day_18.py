from collections import deque
from itertools import islice

from typing_extensions import TypeAlias

SAFE: bool = False
TRAP: bool = True
Tile: TypeAlias = bool


# From https://docs.python.org/3/library/itertools.html#itertools-recipes
def sliding_window(iterable, n):
    """Collect data into overlapping fixed-length chunks or blocks."""
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def get_safe_tile_nbr(first_row: list[Tile], row_nbr: int) -> int:
    safe_patterns = {
        (TRAP, TRAP, SAFE),
        (SAFE, TRAP, TRAP),
        (TRAP, SAFE, SAFE),
        (SAFE, SAFE, TRAP),
    }
    safe_tile_nbr = sum(1 for tile in first_row if tile == SAFE)
    old_row = [SAFE] + first_row + [SAFE]
    new_row: list[Tile] = [SAFE] * len(old_row)
    for _ in range(row_nbr - 1):
        for idx, (a, b, c) in enumerate(sliding_window(old_row, 3)):
            if (a, b, c) in safe_patterns:
                new_row[idx + 1] = TRAP
            else:
                new_row[idx + 1] = SAFE
                safe_tile_nbr += 1

        for i in range(len(old_row)):
            old_row[i] = new_row[i]
    return safe_tile_nbr


def part_one(first_row: list[Tile]) -> int:
    return get_safe_tile_nbr(first_row, 40)


def part_two(first_row: list[Tile]) -> int:
    return get_safe_tile_nbr(first_row, 400000)


def parse_input(file_path: str) -> list[Tile]:
    with open(file_path) as f:
        return [c == "^" for c in f.readline().strip()]


def main():
    first_row = parse_input("input_part_1.txt")
    result_1 = part_one(first_row)
    print(f"Result part 1: {result_1}")

    first_row = parse_input("input_part_2.txt")
    result_2 = part_two(first_row)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
