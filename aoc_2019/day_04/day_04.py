from itertools import pairwise


def is_number_valid_p1(number: int) -> bool:
    has_pair = False
    for a, b in pairwise(str(number)):
        if b < a:
            return False
        if a == b:
            has_pair = True
    return has_pair


def part_one(start: int, end: int) -> int:
    return sum(is_number_valid_p1(n) for n in range(start, end + 1))


def is_number_valid_p2(number: int) -> bool:
    has_pair = False
    repeat_count = 0
    for a, b in pairwise(str(number)):
        if b < a:
            return False
        if a == b:
            repeat_count += 1
        else:
            if repeat_count == 1:
                has_pair = True
            repeat_count = 0
    if repeat_count == 1:
        has_pair = True
    return has_pair


def part_two(start: int, end: int) -> int:
    return sum(is_number_valid_p2(n) for n in range(start, end + 1))


def parse_input(filename: str) -> tuple[int, int]:
    with open(filename) as f:
        start, end = f.read().strip().split("-")
        return int(start), int(end)


def main():
    start, end = parse_input("input_part_1.txt")
    result_1 = part_one(start, end)
    print(f"Result part 1: {result_1}")

    start, end = parse_input("input_part_2.txt")
    result_2 = part_two(start, end)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
