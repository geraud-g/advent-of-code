import operator


def get_value(intcode: list[int], parameter_mode: int, parameter: int) -> int:
    val = intcode[parameter]
    if parameter_mode == 1:
        return val
    else:
        return intcode[val]


def process(intcode: list[int], process_input: list[int]) -> int:  # noqa: PLR0912
    instruction_ptr = 0
    process_output = []

    while True:
        value = intcode[instruction_ptr]
        parameter_mode_a = value // 100 % 10
        parameter_mode_b = value // 1000 % 10
        instruction = value % 100
        ops = {1: operator.add, 2: operator.mul, 7: operator.lt, 8: operator.eq}

        match instruction:
            case 1 | 2:  # Add | Mult
                pos_a = get_value(intcode, parameter_mode_a, instruction_ptr + 1)
                pos_b = get_value(intcode, parameter_mode_b, instruction_ptr + 2)
                output = intcode[instruction_ptr + 3]
                op = ops[instruction]
                intcode[output] = op(pos_a, pos_b)
                instruction_ptr += 4
            case 3:  # Input value
                pos_a = intcode[instruction_ptr + 1]
                intcode[pos_a] = process_input.pop()
                instruction_ptr += 2
            case 4:  # Output value
                pos_a = get_value(intcode, parameter_mode_a, instruction_ptr + 1)
                process_output.append(pos_a)
                instruction_ptr += 2
            case 5:  # Jump if True
                pos_a = get_value(intcode, parameter_mode_a, instruction_ptr + 1)
                if pos_a != 0:
                    instruction_ptr = get_value(
                        intcode, parameter_mode_b, instruction_ptr + 2
                    )
                else:
                    instruction_ptr += 3
            case 6:  # Jump if False
                pos_a = get_value(intcode, parameter_mode_a, instruction_ptr + 1)
                if pos_a == 0:
                    instruction_ptr = get_value(
                        intcode, parameter_mode_b, instruction_ptr + 2
                    )
                else:
                    instruction_ptr += 3
            case 7 | 8:  # Less than | Equals
                pos_a = get_value(intcode, parameter_mode_a, instruction_ptr + 1)
                pos_b = get_value(intcode, parameter_mode_b, instruction_ptr + 2)
                op = ops[instruction]
                if op(pos_a, pos_b):
                    intcode[intcode[instruction_ptr + 3]] = 1
                else:
                    intcode[intcode[instruction_ptr + 3]] = 0
                instruction_ptr += 4
            case 99:  # Break
                break
            case _:
                raise ValueError(f"Invalid opcode: {instruction}")

    return process_output[-1]


def part_one(intcode: list[int]) -> int | None:
    return process(intcode, [1])


def part_two(intcode: list[int]) -> int | None:
    return process(intcode, [5])


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
