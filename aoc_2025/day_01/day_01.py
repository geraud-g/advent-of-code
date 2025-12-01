def part_one(document: list[int]):
    dial = 50
    password = 0
    for value in document:
        dial = (dial + value) % 100
        if dial == 0:
            password += 1
    return password


def part_two(document: list[int]):
    dial = 50
    password = 0
    for value in document:
        modifier = -1 if value < 0 else 1
        for _ in range(abs(value)):
            dial = (dial + modifier) % 100
            if dial == 0:
                password += 1
    return password


def parse_input(filename: str) -> list[int]:
    output = []
    with open(filename) as f:
        for line in f.readlines():
            value = int(line[1:])
            if line[0] == "L":
                value = -value
            output.append(value)
    return output


def main():
    document = parse_input("input_part_1.txt")
    result_1 = part_one(document)
    print(f"Result part 1: {result_1}")

    document = parse_input("input_part_2.txt")
    result_2 = part_two(document)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
