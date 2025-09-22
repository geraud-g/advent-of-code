import re
from dataclasses import dataclass, field


class Instruction:
    pass


@dataclass
class Copy(Instruction):
    x: str | int
    y: str


@dataclass
class Inc(Instruction):
    x: str


@dataclass
class Dec(Instruction):
    x: str


@dataclass
class JumpIfNotZero(Instruction):
    x: str | int
    y: int


@dataclass
class ProgramState:
    registers: dict[str, int] = field(
        default_factory=lambda: {
            "a": 0,
            "b": 0,
            "c": 0,
            "d": 0,
        }
    )
    instruction_pointer: int = 0

    def run(self, instructions: list[Instruction]) -> None:
        while True:
            try:
                next_instruction = instructions[self.instruction_pointer]
            except IndexError:
                break
            match next_instruction:
                case Copy(x, y):
                    if isinstance(x, str):
                        self.registers[y] = self.registers[x]
                    else:
                        self.registers[y] = x
                    self.instruction_pointer += 1
                case Inc(x):
                    self.registers[x] += 1
                    self.instruction_pointer += 1
                case Dec(x):
                    self.registers[x] -= 1
                    self.instruction_pointer += 1
                case JumpIfNotZero(x, y):
                    if isinstance(x, str):
                        value_to_compare = self.registers[x]
                    else:
                        value_to_compare = x
                    if value_to_compare != 0:
                        self.instruction_pointer += y
                    else:
                        self.instruction_pointer += 1


def part_one(instructions: list[Instruction]) -> int:
    program = ProgramState()
    program.run(instructions)
    return program.registers["a"]


def part_two(instructions: list[Instruction]) -> int:
    program = ProgramState()
    program.registers["c"] = 1
    program.run(instructions)
    return program.registers["a"]


def parse_input(file_path: str) -> list[Instruction]:
    regex_cpy = re.compile(r"cpy ([abcd]|-?\d+) ([abcd])")
    regex_inc = re.compile(r"inc ([abcd])")
    regex_dec = re.compile(r"dec ([abcd])")
    regex_jnz = re.compile(r"jnz ([abcd]|-?\d+) (-?\d+)")

    with open(file_path) as f:
        lines = f.readlines()

    instructions = []
    for line in lines:
        if match := regex_cpy.match(line):
            value = match.group(1)
            if value not in ("a", "b", "c", "d"):
                value = int(value)
            instructions.append(Copy(value, match.group(2)))
        elif match := regex_inc.match(line):
            instructions.append(Inc(match.group(1)))
        elif match := regex_dec.match(line):
            instructions.append(Dec(match.group(1)))
        elif match := regex_jnz.match(line):
            value = match.group(1)
            if value not in ("a", "b", "c", "d"):
                value = int(value)
            instructions.append(JumpIfNotZero(value, int(match.group(2))))
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
