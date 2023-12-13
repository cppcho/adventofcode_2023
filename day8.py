import re
import functools
import heapq
import collections
import enum


class Solver:
    def __init__(self, file_name):
        self.file_name = file_name

        self.lines = []
        with open(self.file_name, "r", encoding="utf-8") as file:
            for line in file:
                self.lines.append(line.strip())

    def part_one(self):
        instructions = self.lines[0]
        nodes = {}

        for line in self.lines[2:]:
            matches = re.search(r"(\w+) = \((\w+), (\w+)\)", line)
            assert matches is not None
            key, left, right = matches.groups()
            nodes[key] = (left, right)

        current = "AAA"
        count = 0
        next_instruction = 0
        while current != "ZZZ":
            if instructions[next_instruction] == "L":
                current = nodes[current][0]
            else:
                current = nodes[current][1]
            next_instruction = next_instruction + 1
            if next_instruction == len(instructions):
                next_instruction = 0
            count = count + 1

        return count

    def part_two(self):
        return 0


if __name__ == "__main__":
    example_solver = Solver("data/day8_input_example.txt")
    solver = Solver("data/day8_input.txt")
    print(f"Q1 (Example): {example_solver.part_one()}")
    # print(f"Q2 (Example): {example_solver.part_two()}")
    print(f"Q1: {solver.part_one()}")
    # print(f"Q2: {solver.part_two()}")
