import re


class Solver:
    def __init__(self, file_name):
        self.file_name = file_name

        self.lines = []
        with open(self.file_name, "r", encoding="utf-8") as file:
            for line in file:
                self.lines.append(line.strip())

    def part_one(self):
        times = (int(i) for i in re.findall(r"\d+", self.lines[0]))
        distances = (int(i) for i in re.findall(r"\d+", self.lines[1]))

        output = 1
        for time, distance in zip(times, distances):
            for t in range(1, time):
                d = t * (time - t)
                if d > distance:
                    output = output * (time - 2 * t + 1)
                    break
        return output

    def part_two(self):
        times = re.findall(r"\d+", self.lines[0])
        distances = re.findall(r"\d+", self.lines[1])
        time = int("".join(times))
        distance = int("".join(distances))
        print(time)
        print(distance)
        for t in range(1, time):
            d = t * (time - t)
            if d > distance:
                return time - 2 * t + 1


if __name__ == "__main__":
    example_solver = Solver("data/day6_input_example.txt")
    solver = Solver("data/day6_input.txt")
    print(f"Q1 (Example): {example_solver.part_one()}")
    print(f"Q2 (Example): {example_solver.part_two()}")
    print(f"Q1: {solver.part_one()}")
    print(f"Q2: {solver.part_two()}")
