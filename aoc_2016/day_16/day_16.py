from itertools import islice


# From https://docs.python.org/3.11/library/itertools.html#itertools-recipes
def batched(iterable, n):
    """Batch data into tuples of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


# From https://stackoverflow.com/a/78873321
def reverse_bits(n, w):
    transtable = bytes([int(f"{i:08b}"[::-1], 2) for i in range(256)])
    rem = w % 8
    if rem:
        # peel off the low bits and flip them separately
        low = n & ((1 << rem) - 1)
        hi = n >> rem
        hirev = int.from_bytes(
            hi.to_bytes(w // 8, "little").translate(transtable), "big"
        )
        shift = w - rem - (8 - rem)
        if shift < 0:
            return hirev | (transtable[low] >> -shift)
        else:
            return hirev | (transtable[low] << shift)
    else:
        return int.from_bytes(n.to_bytes(w // 8, "little").translate(transtable), "big")


def process_single_step(state: int, state_length: int) -> int:
    right_part = reverse_bits(state, state_length)
    right_part = right_part ^ ((1 << state_length) - 1)
    # Shift all the bits and one for the new 0
    state = state << (state_length + 1)
    state = state | right_part
    return state


def get_checksum(initial_state: int, length: int) -> int:
    checksum = ""
    state = bin(initial_state)[2:]
    state = state.rjust(length, "0")
    for a, b in batched(state, 2):
        if a == b:
            checksum += "1"
        else:
            checksum += "0"
    return int(checksum, 2)


def part_one(initial_state: int, targeted_length: int) -> str:
    state = initial_state
    state_length = state.bit_length()

    while state_length < targeted_length:
        state = process_single_step(state, state_length)
        state_length = (state_length * 2) + 1

    # Trim to the targeted length
    if state_length > targeted_length:
        state = state >> (state_length - targeted_length)

    checksum = get_checksum(state, targeted_length)
    state_length = targeted_length / 2

    while state_length % 2 == 0:
        checksum = get_checksum(checksum, int(state_length))
        state_length = state_length / 2

    return bin(checksum)[2:].rjust(int(state_length), "0")


def parse_input(file_path: str) -> int:
    with open(file_path) as f:
        return int(f.readline(), 2)


def main():
    initial_state = parse_input("input_part_1.txt")
    result_1 = part_one(initial_state, 272)
    print(f"Result part 1: {result_1}")

    initial_state = parse_input("input_part_2.txt")
    result_2 = part_one(initial_state, 35651584)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
