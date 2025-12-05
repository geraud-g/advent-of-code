from typing import TypeAlias

FreshIngredientRange: TypeAlias = tuple[int, int]


def is_fresh(fresh_ranges: list[FreshIngredientRange], ingredient: int) -> bool:
    return any(start <= ingredient <= end for start, end in fresh_ranges)


def part_one(fresh_ranges: list[FreshIngredientRange], ingredients: list[int]) -> int:
    return len([i for i in ingredients if is_fresh(fresh_ranges, i)])


def part_two(fresh_ranges: list[FreshIngredientRange]) -> int:
    fresh_ranges = sorted(fresh_ranges)
    start, end = fresh_ranges[0]
    fresh_ingredients = end - start + 1

    for current_start, current_end in fresh_ranges[1:]:
        if current_end <= start or current_end <= end:
            continue
        start = (end + 1) if current_start <= end else current_start
        end = current_end
        fresh_ingredients += end - start + 1

    return fresh_ingredients


def parse_input(filename: str) -> tuple[list[FreshIngredientRange], list[int]]:
    fresh_ranges = []
    with open(filename) as f:
        file = f.read().split("\n\n")
        for ingredient_range in file[0].split("\n"):
            fresh_ranges.append(tuple(map(int, ingredient_range.split("-"))))
        ingredients = list(map(int, file[1].strip().split("\n")))
    return fresh_ranges, ingredients


def main():
    fresh_ranges, ingredients = parse_input("input_part_1.txt")
    result_1 = part_one(fresh_ranges, ingredients)
    print(f"Result part 1: {result_1}")

    fresh_ranges, ingredients = parse_input("input_part_2.txt")
    result_2 = part_two(fresh_ranges)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
