def part_one(masses: list[int]) -> int:
    return sum(mass // 3 - 2 for mass in masses)


def get_mass_rec(mass: int) -> int:
    fuel_required = (mass // 3) - 2
    if fuel_required > 0:
        return get_mass_rec(fuel_required) + fuel_required
    else:
        return 0


def part_two(masses: list[int]) -> int:
    return sum(get_mass_rec(mass) for mass in masses)


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


def main():
    masses = parse_input("input_part_1.txt")
    result_1 = part_one(masses)
    print(f"Result part 1: {result_1}")

    masses = parse_input("input_part_2.txt")
    result_2 = part_two(masses)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
