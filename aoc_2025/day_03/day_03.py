def get_largest_joltage(bank: list[int], battery_nbr: int) -> int:
    joltage = 0
    offset = 0

    for i in range(battery_nbr - 1, 0, -1):
        value = max(bank[offset:-i])
        offset = offset + bank[offset:-i].index(value) + 1
        joltage = (joltage + value) * 10
    return joltage + max(bank[offset:])


def part_one(banks: list[list[int]]) -> int:
    return sum(get_largest_joltage(bank, 2) for bank in banks)


def part_two(banks: list[list[int]]):
    return sum(get_largest_joltage(bank, 12) for bank in banks)


def parse_input(filename: str) -> list[list[int]]:
    banks = []
    with open(filename) as f:
        for line in f.readlines():
            banks.append(list(map(int, line.strip())))
    return banks


def main():
    banks = parse_input("input_part_1.txt")
    result_1 = part_one(banks)
    print(f"Result part 1: {result_1}")

    banks = parse_input("input_part_2.txt")
    result_2 = part_two(banks)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
