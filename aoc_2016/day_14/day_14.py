from dataclasses import dataclass
from hashlib import md5


@dataclass(frozen=True)
class CachedHash:
    digest: str
    repeated_char: str | None


def get_triple_repeat(digest: str) -> str | None:
    for idx, char in enumerate(digest[:-2]):
        if char == digest[idx + 1] == digest[idx + 2]:
            return char
    return None


def get_or_compute_hash(
    cache: dict[int, CachedHash], salt: str, index: int, stretch: bool = False
) -> CachedHash:
    if index in cache:
        return cache[index]

    to_eval = f"{salt}{index}"
    to_eval_hash = md5(to_eval.encode()).hexdigest()
    if stretch:
        for _ in range(2016):
            to_eval_hash = md5(to_eval_hash.encode()).hexdigest()
    repeated_char = get_triple_repeat(to_eval_hash)

    cached_hash = CachedHash(digest=to_eval_hash, repeated_char=repeated_char)
    cache[index] = cached_hash
    return cached_hash


def is_valid_key(
    cache: dict[int, CachedHash], salt: str, current_index: int, stretch: bool
) -> bool:
    cached_hash = get_or_compute_hash(cache, salt, current_index, stretch)
    if not cached_hash.repeated_char:
        return False
    repeated_char = cached_hash.repeated_char * 5
    for i in range(current_index + 1, current_index + 1001):
        other_hash = get_or_compute_hash(cache, salt, i, stretch)
        if repeated_char in other_hash.digest:
            return True
    return False


def compute_key(salt: str, stretch: bool) -> int:
    keys = []
    cache = dict()

    for i in range(1_000_000_000):  # Arbitrary large number
        if is_valid_key(cache, salt, i, stretch):
            keys.append(i)
            if len(keys) == 64:
                return i
    raise ValueError("No valid keys found")


def parse_input(file_path: str) -> str:
    with open(file_path) as f:
        return f.readline().strip()


def main():
    salt = parse_input("input_part_1.txt")
    result_1 = compute_key(salt, False)
    print(f"Result part 1: {result_1}")

    salt = parse_input("input_part_2.txt")
    result_2 = compute_key(salt, True)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
