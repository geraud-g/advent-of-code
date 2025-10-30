from collections import Counter
from itertools import combinations


def part_one(boxes: list[str]) -> int:
    doubles = 0
    triples = 0
    for line in boxes:
        counter = Counter(line)
        values = counter.values()
        doubles += any([1 for value in values if value == 2])
        triples += any([1 for value in values if value == 3])
    return doubles * triples


def part_two(boxes: list[str]) -> str:
    for box_a, box_b in combinations(boxes, 2):
        diff_letters = sum(1 for x, y in zip(box_a, box_b, strict=False) if x != y)
        if diff_letters == 1:
            return "".join(c for c in box_a if c in box_b)
    raise ValueError("Can't find a solution for part two")


def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return [n.strip() for n in f.readlines()]


def main():
    boxes = parse_input("input_part_1.txt")
    result_1 = part_one(boxes)
    print(f"Result part 1: {result_1}")

    boxes = parse_input("input_part_2.txt")
    result_2 = part_two(boxes)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
