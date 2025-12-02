import re

PATTERN_PART_1 = re.compile(r"^(\d+)\1$")
PATTERN_PART_2 = re.compile(r"^(\d+)\1+$")


def sum_invalid_ids_in_range(
    range_start: int, range_end: int, pattern: re.Pattern
) -> int:
    invalid_id_count = 0
    for value in range(range_start, range_end + 1):
        if pattern.match(str(value)):
            invalid_id_count += value
    return invalid_id_count


def part_one(id_ranges: list[list[int]]) -> int:
    invalid_ids = 0
    for id_range_start, id_range_end in id_ranges:
        invalid_ids += sum_invalid_ids_in_range(
            id_range_start, id_range_end, PATTERN_PART_1
        )
    return invalid_ids


def part_two(id_ranges: list[list[int]]) -> int:
    invalid_ids = 0
    for id_range_start, id_range_end in id_ranges:
        invalid_ids += sum_invalid_ids_in_range(
            id_range_start, id_range_end, PATTERN_PART_2
        )
    return invalid_ids


def parse_input(filename: str) -> list[list[int]]:
    ranges = []
    with open(filename) as f:
        raw_ranges = f.readline().split(",")
        for raw_range in raw_ranges:
            id_range = [int(value) for value in raw_range.split("-")]
            assert len(id_range) == 2
            ranges.append(id_range)
    return ranges


def main():
    id_ranges = parse_input("input_part_1.txt")
    result_1 = part_one(id_ranges)
    print(f"Result part 1: {result_1}")

    id_ranges = parse_input("input_part_2.txt")
    result_2 = part_two(id_ranges)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
