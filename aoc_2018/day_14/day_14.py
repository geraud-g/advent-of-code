def part_one(recipes_nbr: int) -> str:
    # score_board = [int(c) for c in chr(recipes)]
    elf_1_idx = 0
    elf_2_idx = 1
    current_recipes = 2
    recipes = [3, 7]

    while current_recipes < recipes_nbr + 10:
        new_recipe = recipes[elf_1_idx] + recipes[elf_2_idx]
        # print(f"{recipes}, [{new_recipe}]")
        if new_recipe > 9:
            recipes.append(new_recipe // 10)
            recipes.append(new_recipe % 10)
            current_recipes += 2
        else:
            recipes.append(new_recipe)
            current_recipes += 1
        elf_1_idx = (elf_1_idx + 1 + recipes[elf_1_idx]) % len(recipes)
        elf_2_idx = (elf_2_idx + 1 + recipes[elf_2_idx]) % len(recipes)
    return "".join(map(str, recipes[recipes_nbr : recipes_nbr + 10]))


def contains_recipe(recipes: list[int], recipe_to_get: list[int]) -> bool:
    recipe_to_get_len = len(recipe_to_get)
    for idx in range(len(recipes)):
        if recipes[idx : idx + recipe_to_get_len] == recipe_to_get:
            return True
    return False


def part_two(recipes_nbr: int) -> int:
    elf_1_idx = 0
    elf_2_idx = 1
    recipes = [3, 7]
    recipe_to_get = [int(c) for c in str(recipes_nbr)]
    recipe_to_get_len = len(recipe_to_get)

    for _iteration in range(1_000_000_000):
        new_recipe = recipes[elf_1_idx] + recipes[elf_2_idx]
        if new_recipe > 9:
            recipes.append(new_recipe // 10)
            if (
                len(recipes) >= recipe_to_get_len
                and recipes[-recipe_to_get_len:] == recipe_to_get
            ):
                return len(recipes) - recipe_to_get_len
            recipes.append(new_recipe % 10)
            if (
                len(recipes) >= recipe_to_get_len
                and recipes[-recipe_to_get_len:] == recipe_to_get
            ):
                return len(recipes) - recipe_to_get_len
        else:
            recipes.append(new_recipe)
            if (
                len(recipes) >= recipe_to_get_len
                and recipes[-recipe_to_get_len:] == recipe_to_get
            ):
                return len(recipes) - recipe_to_get_len
        elf_1_idx = (elf_1_idx + 1 + recipes[elf_1_idx]) % len(recipes)
        elf_2_idx = (elf_2_idx + 1 + recipes[elf_2_idx]) % len(recipes)

    raise ValueError


def parse_input(filename: str) -> int:
    with open(filename) as f:
        return int(f.readline())


def main():
    recipes = parse_input("input_part_1.txt")
    result_1 = part_one(recipes)
    print(f"Result part 1: {result_1}")

    recipes = parse_input("input_part_2.txt")
    result_2 = part_two(recipes)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
