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
class Out(Instruction):
    x: Val


@dataclass
class ProgramState:
    registers: dict[str, int] = field(
        default_factory=lambda: {"a": 0, "b": 0, "c": 0, "d": 0}
    )
    instruction_pointer: int = 0
    last_output: int = 1

    def get_value(self, x: Val) -> int:
        return self.registers[x] if isinstance(x, str) else x

    def in_bounds(self, idx: int, instructions: List[Instruction]) -> bool:
        return 0 <= idx < len(instructions)

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

    def op_out(self, instr: Out, instructions: List[Instruction]) -> None:
        self.last_output = self.get_value(instr.x)
        self.instruction_pointer += 1

    def step(self, instructions: List[Instruction]) -> bool:
        """Execute a single instruction; return False if halted"""
        if not self.in_bounds(self.instruction_pointer, instructions):
            return False

        instr = instructions[self.instruction_pointer]
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
                case Out():
                    output_before = self.last_output
                    self.op_out(instr, instructions)
                    if output_before == self.last_output:
                        return False
        except IndexError:
            self.instruction_pointer += 1
        return True

    def get_signature(self) -> tuple[int, ...]:
        return (
            self.instruction_pointer,
            self.registers["a"],
            self.registers["b"],
            self.registers["c"],
            self.registers["d"],
        )

    def run(self, instructions: List[Instruction]) -> bool:
        states = {self.get_signature()}
        while self.step(instructions):
            new_state = self.get_signature()
            if new_state in states:
                return True
            states.add(new_state)
        return False


def part_one(instructions: List[Instruction]) -> int:
    for a_value in range(1_000_000):  # Arbitrary high value
        program = ProgramState()
        program.registers["a"] = a_value
        if program.run(instructions.copy()):
            return a_value
    raise ValueError("Cannot find solution for part 1")


def parse_input(file_path: str) -> List[Instruction]:
    regex_cpy = re.compile(r"cpy ([abcd]|-?\d+) ([abcd])")
    regex_inc = re.compile(r"inc ([abcd])")
    regex_dec = re.compile(r"dec ([abcd])")
    regex_jnz = re.compile(r"jnz ([abcd]|-?\d+) ([abcd]|-?\d+)")
    regex_out = re.compile(r"out ([abcd])")

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
        elif match := regex_out.match(line):
            instructions.append(Out(match.group(1)))
        else:
            raise ValueError(f"Invalid instruction: {line}")
    return instructions


def main():
    instructions = parse_input("input_part_1.txt")
    result_1 = part_one(instructions)
    print(f"Result part 1: {result_1}")


if __name__ == "__main__":
    main()
