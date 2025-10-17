def part_one(changes: list[int]) -> int:
    return sum(changes)


def part_two(changes: list[int]) -> int:
    frequency_history = {0}
    frequency = 0
    for _ in range(1_000_000):  # Arbitrary high number
        for change in changes:
            frequency += change
            if frequency in frequency_history:
                return frequency
            frequency_history.add(frequency)
    raise ValueError("No solution found for part two")


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(n) for n in f.readlines()]


def main():
    changes = parse_input("input_part_1.txt")
    result_1 = part_one(changes)
    print(f"Result part 1: {result_1}")

    changes = parse_input("input_part_2.txt")
    result_2 = part_two(changes)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
