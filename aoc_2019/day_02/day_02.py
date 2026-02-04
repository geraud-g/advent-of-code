def process(intcode: list[int]):
    instruction_ptr = 0

    while True:
        value = intcode[instruction_ptr]
        match value:
            case 1:
                pos_a = intcode[instruction_ptr + 1]
                pos_b = intcode[instruction_ptr + 2]
                output = intcode[instruction_ptr + 3]
                intcode[output] = intcode[pos_a] + intcode[pos_b]
            case 2:
                pos_a = intcode[instruction_ptr + 1]
                pos_b = intcode[instruction_ptr + 2]
                output = intcode[instruction_ptr + 3]
                intcode[output] = intcode[pos_a] * intcode[pos_b]
            case 99:
                break
            case _:
                raise ValueError(f"Invalid opcode: {value}")
        instruction_ptr += 4


def part_one(intcode: list[int]) -> int | None:
    intcode[1] = 12
    intcode[2] = 2
    try:
        process(intcode)
    except (ValueError, IndexError):
        return None
    return intcode[0]


def part_two(intcode: list[int]) -> int | None:
    for noun in range(100):
        for verb in range(100):
            intcode_cpy = intcode.copy()
            intcode_cpy[1] = noun
            intcode_cpy[2] = verb
            try:
                process(intcode_cpy)
            except (ValueError, IndexError):
                return None
            if intcode_cpy[0] == 19690720:
                return 100 * noun + verb
    raise ValueError("No solution found for part two")


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return [int(c) for c in f.readline().split(",")]


def main():
    data = parse_input("input_part_1.txt")
    result_1 = part_one(data)
    print(f"Result part 1: {result_1}")

    data = parse_input("input_part_2.txt")
    result_2 = part_two(data)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
