from hashlib import md5


def part_one(door_id: str) -> str:
    password = []
    for current_idx in range(1_000_000_000):  # Arbitrary high value
        door_with_id = door_id + str(current_idx)
        hashed = md5(door_with_id.encode()).hexdigest()
        if not hashed.startswith("00000"):
            continue
        password.append(hashed[5])
        if len(password) == 8:
            return "".join(map(str, password))
    raise ValueError(f"Cannot find password for door id `{door_id}`")


def part_two(door_id: str) -> str:
    password = [""] * 8
    found_chars = 0
    for current_idx in range(1_000_000_000):  # Arbitrary high value
        door_with_id = door_id + str(current_idx)
        hashed = md5(door_with_id.encode()).hexdigest()
        if not hashed.startswith("00000"):
            continue
        try:
            char_idx = int(hashed[5])
        except ValueError:
            char_idx = 9
        if char_idx < 8 and not password[char_idx]:
            password[char_idx] = hashed[6]
            found_chars += 1
            if found_chars == 8:
                return "".join(map(str, password))
    raise ValueError(f"Cannot find password for door id `{door_id}`")


def main():
    with open("input_part_1.txt") as f:
        result_1 = part_one(f.read().strip())
        print(f"Result part 1: {result_1}")

    with open("input_part_2.txt") as f:
        result_2 = part_two(f.read().strip())
        print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
