from collections import deque
from itertools import permutations


class Process:
    def __init__(self, intcode: list[int]):
        self.instruction_ptr = 0
        self.exited = False
        self.intcode = intcode
        self.input = deque()
        self.output = []

    def add_input(self, value: int):
        self.input.append(value)

    def run(self):
        while True:
            value = self.intcode[self.instruction_ptr]
            parameter_mode_a = value // 100 % 10
            parameter_mode_b = value // 1000 % 10
            instruction = value % 100

            match instruction:
                case 1:
                    self.op_add(parameter_mode_a, parameter_mode_b)
                case 2:
                    self.op_mul(parameter_mode_a, parameter_mode_b)
                case 3:
                    self.op_input()
                case 4:
                    self.op_output(parameter_mode_a)
                    break
                case 5:
                    self.op_jump_if_true(parameter_mode_a, parameter_mode_b)
                case 6:
                    self.op_jump_if_false(parameter_mode_a, parameter_mode_b)
                case 7:
                    self.op_less_than(parameter_mode_a, parameter_mode_b)
                case 8:
                    self.op_equals(parameter_mode_a, parameter_mode_b)
                case 99:  # Break
                    self.exited = True
                    break
                case _:
                    raise ValueError(f"Invalid opcode: {instruction}")

    def _get_value(self, parameter_mode: int, instruction_ptr: int) -> int:
        val = self.intcode[instruction_ptr]
        if parameter_mode == 1:
            return val
        else:
            return self.intcode[val]

    def op_add(self, parameter_mode_a: int, parameter_mode_b: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        output = self.intcode[self.instruction_ptr + 3]
        self.intcode[output] = pos_a + pos_b
        self.instruction_ptr += 4

    def op_mul(self, parameter_mode_a: int, parameter_mode_b: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        output = self.intcode[self.instruction_ptr + 3]
        self.intcode[output] = pos_a * pos_b
        self.instruction_ptr += 4

    def op_input(self):
        pos_a = self.intcode[self.instruction_ptr + 1]
        self.intcode[pos_a] = self.input.popleft()
        self.instruction_ptr += 2

    def op_output(self, parameter_mode_a: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        self.output.append(pos_a)
        self.instruction_ptr += 2

    def op_jump_if_true(self, parameter_mode_a: int, parameter_mode_b: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        if pos_a != 0:
            self.instruction_ptr = self._get_value(
                parameter_mode_b, self.instruction_ptr + 2
            )
        else:
            self.instruction_ptr += 3

    def op_jump_if_false(self, parameter_mode_a: int, parameter_mode_b: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        if pos_a == 0:
            self.instruction_ptr = self._get_value(
                parameter_mode_b, self.instruction_ptr + 2
            )
        else:
            self.instruction_ptr += 3

    def op_less_than(self, parameter_mode_a: int, parameter_mode_b: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        if pos_a < pos_b:
            self.intcode[self.intcode[self.instruction_ptr + 3]] = 1
        else:
            self.intcode[self.intcode[self.instruction_ptr + 3]] = 0
        self.instruction_ptr += 4

    def op_equals(self, parameter_mode_a: int, parameter_mode_b: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        if pos_a == pos_b:
            self.intcode[self.intcode[self.instruction_ptr + 3]] = 1
        else:
            self.intcode[self.intcode[self.instruction_ptr + 3]] = 0
        self.instruction_ptr += 4


def part_one(intcode: list[int]) -> int:
    max_signal_value = -1
    for sequence in permutations(range(5)):
        last_output = 0
        for setting in sequence:
            program = Process(intcode.copy())
            program.add_input(setting)
            program.add_input(last_output)
            program.run()
            last_output = program.output[-1]
        max_signal_value = max(last_output, max_signal_value)
    return max_signal_value


def part_two(intcode: list[int]) -> int:
    max_signal_value = -1
    for sequence in permutations(range(5, 10)):
        processes = [Process(intcode.copy()) for _ in range(5)]
        for idx, setting in enumerate(sequence):
            processes[idx].add_input(setting)

        last_output = 0
        current_process_idx = 0
        while not processes[-1].exited:
            processes[current_process_idx].add_input(last_output)
            processes[current_process_idx].run()
            last_output = processes[current_process_idx].output[-1]
            current_process_idx = (current_process_idx + 1) % 5
        max_signal_value = max(processes[-1].output[-1], max_signal_value)

    return max_signal_value


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
