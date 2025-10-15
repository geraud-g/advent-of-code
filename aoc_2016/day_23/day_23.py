import re
from dataclasses import dataclass, field
from typing import Union, List

Val = Union[str, int]


class Instruction:
    pass


@dataclass
class Copy(Instruction):
    x: Val
    y: Val


@dataclass
class Inc(Instruction):
    x: Val


@dataclass
class Dec(Instruction):
    x: Val


@dataclass
class JumpIfNotZero(Instruction):
    x: Val
    y: Val


@dataclass
class Toggle(Instruction):
    x: Val


@dataclass
class ProgramState:
    registers: dict[str, int] = field(
        default_factory=lambda: {"a": 0, "b": 0, "c": 0, "d": 0}
    )
    instruction_pointer: int = 0

    def get_value(self, x: Val) -> int:
        return self.registers[x] if isinstance(x, str) else x

    def in_bounds(self, idx: int, instructions: List[Instruction]) -> bool:
        return 0 <= idx < len(instructions)

    def detect_mul(self, instructions: List[Instruction]) -> bool:
        current_idx = self.instruction_pointer
        if not self.in_bounds(current_idx + 5, instructions):
            return False
        product_dst = None
        factor_a = None
        factor_b = None
        buffer_a = None
        buffer_b = None

        op_1 = instructions[current_idx]
        op_2 = instructions[current_idx + 1]
        op_3 = instructions[current_idx + 2]
        op_4 = instructions[current_idx + 3]
        op_5 = instructions[current_idx + 4]
        op_6 = instructions[current_idx + 5]

        # Op 1
        if not isinstance(op_1, Copy):
            return False
        factor_a = op_1.x
        buffer_b = op_1.y

        if type(op_2) is type(op_3):
            return False
        # Op 2
        if isinstance(op_2, Inc):
            product_dst = op_2.x
        elif isinstance(op_2, Dec):
            buffer_a = op_2.x
        else:
            return False
        # Op 3
        if isinstance(op_3, Inc):
            product_dst = op_3.x
        elif isinstance(op_3, Dec):
            buffer_a = op_3.x
        else:
            return False

        # Op 4
        if isinstance(op_4, JumpIfNotZero):
            if op_4.y != -2:
                return False
        else:
            return False

        # Op 5
        if isinstance(op_5, Dec):
            factor_b = op_5.x
        else:
            return False

        # Op 6
        if isinstance(op_6, JumpIfNotZero):
            if op_6.y != -5:
                return False
        else:
            return False

        if not all([product_dst, factor_a, factor_b, buffer_a]):
            return False
        self.registers[product_dst] += self.get_value(factor_a) * self.get_value(
            factor_b
        )
        self.registers[buffer_a] = 0
        self.registers[buffer_b] = 0
        self.registers[factor_b] = 0
        self.instruction_pointer += 6
        return True

    def op_copy(self, instr: Copy, _instructions: List[Instruction]) -> None:
        if isinstance(instr.y, str):
            self.registers[instr.y] = self.get_value(instr.x)
        self.instruction_pointer += 1

    def op_inc(self, instr: Inc, _instructions: List[Instruction]) -> None:
        if isinstance(instr.x, str):
            self.registers[instr.x] += 1
        self.instruction_pointer += 1

    def op_dec(self, instr: Dec, _instructions: List[Instruction]) -> None:
        if isinstance(instr.x, str):
            self.registers[instr.x] -= 1
        self.instruction_pointer += 1

    def op_jnz(self, instr: JumpIfNotZero, _instructions: List[Instruction]) -> None:
        if self.get_value(instr.x) != 0:
            self.instruction_pointer += self.get_value(instr.y)
        else:
            self.instruction_pointer += 1

    def toggle_at(self, idx: int, instructions: List[Instruction]) -> None:
        target = instructions[idx]
        match target:
            case Inc(x):
                instructions[idx] = Dec(x)
            case Dec(x) | Toggle(x):
                instructions[idx] = Inc(x)
            case Copy(x, y):
                instructions[idx] = JumpIfNotZero(x, y)
            case JumpIfNotZero(x, y):
                instructions[idx] = Copy(x, y)

    def op_tgl(self, instr: Toggle, instructions: List[Instruction]) -> None:
        next_idx = self.instruction_pointer + self.get_value(instr.x)
        if self.in_bounds(next_idx, instructions):
            self.toggle_at(next_idx, instructions)
        self.instruction_pointer += 1

    def step(self, instructions: List[Instruction]) -> bool:
        """Execute a single instruction; return False if halted"""
        if not self.in_bounds(self.instruction_pointer, instructions):
            return False

        instr = instructions[self.instruction_pointer]
        if self.detect_mul(instructions):
            return True
        try:
            match instr:
                case Copy():
                    self.op_copy(instr, instructions)
                case Inc():
                    self.op_inc(instr, instructions)
                case Dec():
                    self.op_dec(instr, instructions)
                case JumpIfNotZero():
                    self.op_jnz(instr, instructions)
                case Toggle():
                    self.op_tgl(instr, instructions)
        except IndexError:
            self.instruction_pointer += 1
        return True

    def run(self, instructions: List[Instruction]) -> None:
        while self.step(instructions):
            pass


def part_one(instructions: List[Instruction]) -> int:
    program = ProgramState()
    program.registers["a"] = 7
    program.run(instructions.copy())
    return program.registers["a"]


def part_two(instructions: List[Instruction]) -> int:
    program = ProgramState()
    program.registers["a"] = 12
    program.run(instructions.copy())
    return program.registers["a"]


def parse_input(file_path: str) -> List[Instruction]:
    regex_cpy = re.compile(r"cpy ([abcd]|-?\d+) ([abcd])")
    regex_inc = re.compile(r"inc ([abcd])")
    regex_dec = re.compile(r"dec ([abcd])")
    regex_jnz = re.compile(r"jnz ([abcd]|-?\d+) ([abcd]|-?\d+)")
    regex_tgl = re.compile(r"tgl ([abcd])")

    with open(file_path) as f:
        lines = f.readlines()

    instructions: List[Instruction] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if match := regex_cpy.match(line):
            x = match.group(1)
            x = int(x) if x not in ("a", "b", "c", "d") else x
            y = match.group(2)
            instructions.append(Copy(x, y))
        elif match := regex_inc.match(line):
            instructions.append(Inc(match.group(1)))
        elif match := regex_dec.match(line):
            instructions.append(Dec(match.group(1)))
        elif match := regex_jnz.match(line):
            x = match.group(1)
            x = int(x) if x not in ("a", "b", "c", "d") else x
            y = match.group(2)
            y = int(y) if y not in ("a", "b", "c", "d") else y
            instructions.append(JumpIfNotZero(x, y))
        elif match := regex_tgl.match(line):
            instructions.append(Toggle(match.group(1)))
        else:
            raise ValueError(f"Invalid instruction: {line}")
    return instructions


def main():
    instructions = parse_input("input_part_1.txt")
    result_1 = part_one(instructions)
    print(f"Result part 1: {result_1}")

    instructions = parse_input("input_part_2.txt")
    result_2 = part_two(instructions)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
