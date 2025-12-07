from operator import add, mul


def solve_problems(problems_values: list[list[int]], operators: list[str]) -> int:
    total_answers = 0
    for i, problem_values in enumerate(problems_values):
        if operators[i] == "*":
            problem_answer = 1
            operation = mul
        else:
            problem_answer = 0
            operation = add
        for value in problem_values:
            problem_answer = operation(problem_answer, value)
        total_answers += problem_answer
    return total_answers


def parse_input_part_1(filename: str) -> tuple[list[list[int]], list[str]]:
    problem_values = []
    with open(filename) as f:
        file = f.readlines()
        for line in file[:-1]:
            problem_values.append(list(map(int, line.split())))
        operators = file[-1].split()
    problem_values = [list(t) for t in zip(*problem_values[::-1], strict=True)]
    return problem_values, operators


def get_problems_values(block: list[str]) -> list[list[int]]:
    problems = []
    current_values = []
    for x in range(len(block[0])):
        current_value = ""
        for y in range(len(block)):
            current_value += block[y][x]
        if not current_value.strip():
            problems.append(current_values)
            current_values = []
        else:
            current_values.append(int(current_value))
    if current_values:
        problems.append(current_values)
    return problems


def parse_input_part_2(filename: str) -> tuple[list[list[int]], list[str]]:
    problems_values = []
    with open(filename) as f:
        file = f.readlines()
        block = file[:-1]
        problems_values = get_problems_values(block)
        operators = file[-1].split()
    return problems_values, operators


def main():
    problems_values, operators = parse_input_part_1("input_part_1.txt")
    result_1 = solve_problems(problems_values, operators)
    print(f"Result part 1: {result_1}")

    problems_values, operators = parse_input_part_2("input_part_2.txt")
    result_2 = solve_problems(problems_values, operators)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
