import re
from collections import OrderedDict
from dataclasses import dataclass, field


@dataclass
class Node:
    id: str
    dependencies: set[str] = field(default_factory=set)


def part_one(nodes: dict[str, Node]) -> str:
    nodes = OrderedDict(sorted(nodes.items()))
    candidates = sorted(nodes.keys())
    stack = []
    while candidates:
        for candidate in candidates:
            node = nodes[candidate]
            if all(d in stack for d in node.dependencies):
                stack.append(candidate)
                candidates.remove(candidate)
                break

    return "".join(stack)


def part_two(nodes: dict[str, Node], nodes_oder: str) -> int:
    elapsed_time = -1
    nodes_progression = {n: ord(n) - 64 + 60 for n in nodes_oder}
    workers = {i: None for i in range(5)}
    completed_nodes = set()
    while any(v > 0 for v in nodes_progression.values()):
        elapsed_time += 1
        for worker_id, target_id in workers.items():
            if target_id is None:
                continue
            if nodes_progression[target_id] > 0:
                nodes_progression[target_id] -= 1
            if nodes_progression[target_id] == 0:
                workers[worker_id] = None
                completed_nodes.add(target_id)

        for key, value in nodes_progression.items():
            if value == 0:
                continue
            node = nodes[key]
            if all(n in completed_nodes for n in node.dependencies):
                for worker_id, target_id in workers.items():
                    if target_id is None and key not in workers.values():
                        workers[worker_id] = key
                        break

    return elapsed_time


def parse_input(filename: str) -> dict[str, Node]:
    nodes = dict()
    pattern = re.compile(r"Step (.) must be finished before step (.) can begin.")
    with open(filename) as f:
        for line in f.readlines():
            if result := pattern.search(line):
                node_id = result.group(1)
                unlocks = result.group(2)
                if node_id not in nodes:
                    nodes[node_id] = Node(node_id)
                if unlocks not in nodes:
                    nodes[unlocks] = Node(unlocks)
                nodes[unlocks].dependencies.add(node_id)
    return nodes


def main():
    nodes = parse_input("input_part_1.txt")
    result_1 = part_one(nodes)
    print(f"Result part 1: {result_1}")

    nodes = parse_input("input_part_2.txt")
    result_2 = part_two(nodes, result_1)
    print(f"Result part 2: {result_2}")


if __name__ == "__main__":
    main()
