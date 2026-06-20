from lib.intcode import Process


def part_one(intcode: list[int]):
    program = Process(intcode, program_input=[1])
    program.run()
    return program.output[-1]


def part_two(intcode: list[int]):
    program = Process(intcode, program_input=[2])
    program.run()
    return program.output[-1]


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(c) for c in f.readline().split(",")]


def main():
    intcode = parse_input("input_part_1.txt")
    result_1 = part_one(intcode)
    print(f"Result part 1: {result_1}")

    intcode = parse_input("input_part_2.txt")
    result_2 = part_two(intcode)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
