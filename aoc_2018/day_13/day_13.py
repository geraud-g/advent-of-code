from dataclasses import dataclass
from enum import Enum


class Intersection(Enum):
    LEFT = 1
    STRAIGHT = 2
    RIGHT = 3

    def get_next_intersection(self) -> "Intersection":
        if self == Intersection.LEFT:
            return Intersection.STRAIGHT
        elif self == Intersection.STRAIGHT:
            return Intersection.RIGHT
        else:
            return Intersection.LEFT


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def get_from_intersection(self, intersection: Intersection) -> "Direction":
        if intersection == Intersection.STRAIGHT:
            return self
        elif intersection == Intersection.LEFT:
            return Direction(((self.value - 2) % 4) + 1)
        else:  # RIGHT
            return Direction((self.value % 4) + 1)


@dataclass
class Point:
    x: int
    y: int

    def get_from(self, direction: Direction) -> "Point":
        if direction == Direction.UP:
            return Point(self.x, self.y - 1)
        elif direction == Direction.DOWN:
            return Point(self.x, self.y + 1)
        elif direction == Direction.LEFT:
            return Point(self.x - 1, self.y)
        elif direction == Direction.RIGHT:
            return Point(self.x + 1, self.y)

    def copy(self) -> "Point":
        return Point(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"(x={self.x},y={self.y})"


@dataclass
class Cart:
    position: Point
    direction: Direction
    intersection: Intersection = Intersection.LEFT

    def __repr__(self):
        return f"Cart({self.position}, {self.direction.name})"

    def update_position(self, lines: list[list[str]]):  # noqa: PLR0912
        # Move first
        self.position = self.position.get_from(self.direction)

        # Then handle direction
        tile = lines[self.position.y][self.position.x]
        match tile:
            case "-":
                pass  # Continue straight on horizontal track

            case "|":
                pass  # Continue straight on vertical track
            case "/":
                match self.direction:
                    case Direction.LEFT:
                        self.direction = Direction.DOWN
                    case Direction.RIGHT:
                        self.direction = Direction.UP
                    case Direction.UP:
                        self.direction = Direction.RIGHT
                    case Direction.DOWN:
                        self.direction = Direction.LEFT
            case "\\":
                match self.direction:
                    case Direction.LEFT:
                        self.direction = Direction.UP
                    case Direction.RIGHT:
                        self.direction = Direction.DOWN
                    case Direction.UP:
                        self.direction = Direction.LEFT
                    case Direction.DOWN:
                        self.direction = Direction.RIGHT
            case "+":
                self.direction = self.direction.get_from_intersection(self.intersection)
                self.intersection = self.intersection.get_next_intersection()

    def copy(self) -> "Cart":
        return Cart(self.position.copy(), self.direction, self.intersection)

    def __hash__(self):
        return hash((self.position, self.direction, self.intersection))


def simulate_step(
    carts: list[Cart], lines: list[list[str]]
) -> tuple[bool, Point | None]:
    # Sort carts by reading order (top to bottom, left to right)
    carts.sort(key=lambda c: (c.position.y, c.position.x))

    for cart_idx, cart in enumerate(carts):
        cart.update_position(lines)

        # Check collision with already-moved carts this step
        for other_cart in carts[:cart_idx]:
            if cart.position == other_cart.position:
                return True, cart.position

        # # Check collision with not-yet-moved carts this step
        for other_cart in carts[cart_idx + 1 :]:
            if cart.position == other_cart.position:
                return True, cart.position
    return False, None


def part_one(carts: list[Cart], lines: list[list[str]]) -> str:
    max_steps = 100_000
    for _ in range(max_steps):
        collision, point = simulate_step(carts, lines)
        if collision:
            return f"{point.x},{point.y}"
    return f"No collision found after {max_steps} steps"


def simulate_step_with_removal(carts: list[Cart], lines: list[list[str]]) -> list[Cart]:
    # Sort carts by reading order
    carts.sort(key=lambda c: (c.position.y, c.position.x))

    crashed = set()

    for cart_idx, cart in enumerate(carts):
        if cart_idx in crashed:
            continue

        cart.update_position(lines)

        # Check for collisions with all other carts
        for other_cart_idx, other_cart in enumerate(carts):
            if (
                cart_idx != other_cart_idx
                and other_cart_idx not in crashed
                and cart.position == other_cart.position
            ):
                # Both carts crash
                crashed.add(cart_idx)
                crashed.add(other_cart_idx)
                break

    # Return non-crashed carts
    return [cart for i, cart in enumerate(carts) if i not in crashed]


def part_two(carts: list[Cart], lines: list[list[str]]) -> str:
    max_steps = 100_000

    for _ in range(max_steps):
        carts = simulate_step_with_removal(carts, lines)

        if len(carts) == 1:
            last_cart = carts[0]
            return f"{last_cart.position.x},{last_cart.position.y}"
        elif len(carts) == 0:
            return "All carts crashed!"

    return f"Timeout after {max_steps} steps"


def parse_input(filename: str) -> tuple[list[Cart], list[list[str]]]:
    carts = []
    lines = []
    with open(filename) as f:
        for y, line in enumerate(f.readlines()):
            new_line = []
            for x, char in enumerate(line):
                match char:
                    case ">":
                        carts.append(Cart(Point(x, y), Direction.RIGHT))
                        new_line.append("-")
                    case "^":
                        carts.append(Cart(Point(x, y), Direction.UP))
                        new_line.append("|")
                    case "v":
                        carts.append(Cart(Point(x, y), Direction.DOWN))
                        new_line.append("|")
                    case "<":
                        carts.append(Cart(Point(x, y), Direction.LEFT))
                        new_line.append("-")
                    case _:
                        new_line.append(char)
            lines.append(new_line)
    return carts, lines


def main():
    carts, lines = parse_input("input_part_1.txt")
    result_1 = part_one(carts, lines)
    print(f"Result part 1: {result_1}")

    carts, lines = parse_input("input_part_2.txt")
    result_2 = part_two(carts, lines)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
