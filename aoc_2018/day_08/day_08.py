import contextlib
from dataclasses import dataclass, field


@dataclass
class Node:
    children_nbr: int = 0
    metadata_nbr: int = 0
    children: list["Node"] = field(default_factory=list)
    metadata_list: list[int] = field(default_factory=list)


def get_next_node(tree: list[int]) -> tuple[Node, int]:
    children_nbr = tree[0]
    metadata_nbr = tree[1]
    current_idx = 2
    node = Node(children_nbr, metadata_nbr)

    for _ in range(children_nbr):
        new_node, offset = get_next_node(tree[current_idx:])
        node.children.append(new_node)
        current_idx += offset

    for _ in range(metadata_nbr):
        node.metadata_list.append(tree[current_idx])
        current_idx += 1

    return node, current_idx


def get_all_nodes(tree: list[int]) -> list[Node]:
    current_idx = 0
    nodes = []
    while current_idx < len(tree):
        new_node, offset = get_next_node(tree[current_idx:])
        nodes.append(new_node)
        current_idx += offset
    return nodes


def get_metadata_sum(node: Node) -> int:
    metadata_sum = sum(node.metadata_list)
    metadata_sum += sum(get_metadata_sum(child) for child in node.children)
    return metadata_sum


def part_one(tree: list[int]) -> int:
    nodes = get_all_nodes(tree)
    return sum(get_metadata_sum(n) for n in nodes)


def get_metadata_sum_part_2(node: Node) -> int:
    if node.children_nbr == 0:
        return sum(node.metadata_list)
    metadata_sum = 0
    for metadata in node.metadata_list:
        with contextlib.suppress(IndexError):
            metadata_sum += get_metadata_sum_part_2(node.children[metadata - 1])
    return metadata_sum


def part_two(tree: list[int]) -> int:
    nodes = get_all_nodes(tree)
    return sum(get_metadata_sum_part_2(n) for n in nodes)


def parse_input(filename: str) -> list[int]:
    with open(filename) as f:
        return list(map(int, f.readline().split()))


def main():
    tree = parse_input("input_part_1.txt")
    result_1 = part_one(tree)
    print(f"Result part 1: {result_1}")

    tree = parse_input("input_part_2.txt")
    result_2 = part_two(tree)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
