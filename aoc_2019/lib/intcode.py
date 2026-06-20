from collections import defaultdict, deque


class Process:
    def __init__(self, intcode: list[int], program_input: list[int] | None = None):
        self.instruction_ptr = 0
        self.exited = False
        self.intcode = defaultdict(int)
        for idx, val in enumerate(intcode):
            self.intcode[idx] = val
        if program_input:
            self.input = deque(program_input)
        else:
            self.input = deque()
        self.output = []
        self.relative_base = 0

    def add_input(self, value: int):
        self.input.append(value)

    def run_until_output(self):
        while True:
            value = self.intcode[self.instruction_ptr]
            parameter_mode_a = value // 100 % 10
            parameter_mode_b = value // 1000 % 10
            parameter_mode_c = value // 10_000 % 10
            instruction = value % 100

            match instruction:
                case 1:
                    self.op_add(parameter_mode_a, parameter_mode_b, parameter_mode_c)
                case 2:
                    self.op_mul(parameter_mode_a, parameter_mode_b, parameter_mode_c)
                case 3:
                    self.op_input(parameter_mode_a)
                case 4:
                    self.op_output(parameter_mode_a)
                    break
                case 5:
                    self.op_jump_if_true(parameter_mode_a, parameter_mode_b)
                case 6:
                    self.op_jump_if_false(parameter_mode_a, parameter_mode_b)
                case 7:
                    self.op_less_than(
                        parameter_mode_a, parameter_mode_b, parameter_mode_c
                    )
                case 8:
                    self.op_equals(parameter_mode_a, parameter_mode_b, parameter_mode_c)
                case 9:
                    self.op_adjust_relative_base(parameter_mode_a)
                case 99:  # Break
                    self.exited = True
                    break
                case _:
                    raise ValueError(f"Invalid opcode: {instruction}")

    def run(self):
        while not self.exited:
            self.run_until_output()

    def _get_value(self, parameter_mode: int, instruction_ptr: int) -> int:
        val = self.intcode[instruction_ptr]
        if parameter_mode == 1:
            return val
        elif parameter_mode == 2:
            return self.intcode[val + self.relative_base]
        else:
            return self.intcode[val]

    def _get_write_address(self, parameter_mode: int, instruction_ptr: int) -> int:
        val = self.intcode[instruction_ptr]
        if parameter_mode == 2:
            return val + self.relative_base
        return val

    def op_add(
        self, parameter_mode_a: int, parameter_mode_b: int, parameter_mode_c: int
    ):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        output = self._get_write_address(parameter_mode_c, self.instruction_ptr + 3)
        self.intcode[output] = pos_a + pos_b
        self.instruction_ptr += 4

    def op_mul(
        self, parameter_mode_a: int, parameter_mode_b: int, parameter_mode_c: int
    ):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        output = self._get_write_address(parameter_mode_c, self.instruction_ptr + 3)
        self.intcode[output] = pos_a * pos_b
        self.instruction_ptr += 4

    def op_input(self, parameter_mode_a: int):
        pos_a = self._get_write_address(parameter_mode_a, self.instruction_ptr + 1)
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

    def op_less_than(
        self, parameter_mode_a: int, parameter_mode_b: int, parameter_mode_c: int
    ):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        write_addr = self._get_write_address(parameter_mode_c, self.instruction_ptr + 3)
        if pos_a < pos_b:
            self.intcode[write_addr] = 1
        else:
            self.intcode[write_addr] = 0
        self.instruction_ptr += 4

    def op_equals(
        self, parameter_mode_a: int, parameter_mode_b: int, parameter_mode_c: int
    ):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        pos_b = self._get_value(parameter_mode_b, self.instruction_ptr + 2)
        write_addr = self._get_write_address(parameter_mode_c, self.instruction_ptr + 3)
        if pos_a == pos_b:
            self.intcode[write_addr] = 1
        else:
            self.intcode[write_addr] = 0
        self.instruction_ptr += 4

    def op_adjust_relative_base(self, parameter_mode_a: int):
        pos_a = self._get_value(parameter_mode_a, self.instruction_ptr + 1)
        self.relative_base += pos_a
        self.instruction_ptr += 2
