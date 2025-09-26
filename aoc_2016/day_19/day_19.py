def part_one(elves_nbr: int) -> int:
    a = 1
    while a * 2 < elves_nbr:
        a *= 2
    return 2 * (elves_nbr - a) + 1


def part_two(elves_nbr: int) -> int:
    a = 2
    a_prev = 1
    while a < elves_nbr:
        a_next = 3 * a - 2
        a_prev = a
        a = a_next
    return elves_nbr - a_prev + 1


def parse_input(file_path: str) -> int:
    with open(file_path) as f:
        return int(f.readline().strip())


def main():
    elves_nbr = parse_input("input_part_1.txt")
    result_1 = part_one(elves_nbr)
    print(f"Result part 1: {result_1}")

    elves_nbr = parse_input("input_part_2.txt")
    result_2 = part_two(elves_nbr)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
