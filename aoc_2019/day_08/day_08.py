WIDTH: int = 25
HEIGHT: int = 6
LAYER_SIZE: int = WIDTH * HEIGHT

BLACK: int = 0
WHITE: int = 1
TRANSPARENT: int = 2


def part_one(pixels: list[list[int]]) -> int:
    layer_with_min_0 = min(pixels, key=lambda x: x.count(0))
    ones = layer_with_min_0.count(1)
    twos = layer_with_min_0.count(2)
    return ones * twos


def part_two(pixels: list[list[int]]) -> str:
    image = pixels[0].copy()

    for y in range(1, len(pixels)):
        current_layer = pixels[y]
        for x in range(LAYER_SIZE):
            if image[x] == TRANSPARENT:
                image[x] = current_layer[x]

    output = "\n"
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if image[y * WIDTH + x] == BLACK:
                output += "█"
            elif image[y * WIDTH + x] == WHITE:
                output += "░"
            else:
                output += " "
        output += "\n"
    return output


def parse_input(filename: str) -> list[list[int]]:
    with open(filename) as f:
        raw_pixels = [int(c) for c in f.readline()]

    pixels = []
    for y in range(HEIGHT):
        pixels.append(raw_pixels[y * WIDTH : y * WIDTH + WIDTH])
    return [
        raw_pixels[i : i + LAYER_SIZE] for i in range(0, len(raw_pixels), LAYER_SIZE)
    ]


def main():
    pixels = parse_input("input_part_1.txt")
    result_1 = part_one(pixels)
    print(f"Result part 1: {result_1}")

    pixels = parse_input("input_part_2.txt")
    result_2 = part_two(pixels)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
