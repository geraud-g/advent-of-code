from collections import deque


def part_one(initial_polymer: list[int]) -> int:
    stack = deque()

    for unit in initial_polymer:
        if stack and abs(stack[-1] - unit) == 32:
            stack.pop()
        else:
            stack.append(unit)
    return len(stack)


def part_two(initial_polymer: list[int]) -> int:
    smallest_polymer = float("inf")
    for unit in range(ord("A"), ord("Z") + 1):
        trimmed_polymer = [u for u in initial_polymer if u not in (unit, unit + 32)]
        result = part_one(trimmed_polymer)
        smallest_polymer = min(result, smallest_polymer)
    return smallest_polymer


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return list([ord(c) for c in f.readline().strip()])


def main():
    polymer = parse_input("input_part_1.txt")
    result_1 = part_one(polymer)
    print(f"Result part 1: {result_1}")

    polymer = parse_input("input_part_2.txt")
    result_2 = part_two(polymer)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
