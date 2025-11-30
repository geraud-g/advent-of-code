def part_one(data):
    pass


def part_two(data):
    pass


def parse_input(filename: str):
    with open(filename) as f:
        return f.read().strip()


def main():
    data = parse_input("input_part_1.txt")
    result_1 = part_one(data)
    print(f"Result part 1: {result_1}")

    data = parse_input("input_part_2.txt")
    result_2 = part_two(data)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
