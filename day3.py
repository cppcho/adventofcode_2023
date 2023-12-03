from collections import defaultdict

file_path = "data/day3_input.txt"


def is_symbol(char):
    return len(char) == 1 and not char.isdigit() and char != "."


def is_part_num(lines, num, row, col):
    length = len(str(num))

    for r in range(row - 1, row + 2):
        if r >= 0 and r < len(lines):
            for c in range(col - 1, col + length + 1):
                if c >= 0 and c < len(lines[row - 1]):
                    if is_symbol(lines[r][c]):
                        return True

    return False


def search_gears(lines, num, row, col):
    length = len(str(num))
    output = []
    for r in range(row - 1, row + 2):
        if r >= 0 and r < len(lines):
            for c in range(col - 1, col + length + 1):
                if c >= 0 and c < len(lines[row - 1]):
                    if lines[r][c] == "*":
                        output.append([r, c])
    return output


def solve1():
    output = 0
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.strip())

    for row, line in enumerate(lines):
        current_num = 0
        start_col = -1
        for col, char in enumerate(line):
            if char.isdigit():
                if start_col < 0:
                    start_col = col
                current_num = current_num * 10 + int(char)
            else:
                if is_part_num(lines, current_num, row, start_col):
                    output = output + current_num
                current_num = 0
                start_col = -1
        if start_col >= 0:
            if is_part_num(lines, current_num, row, start_col):
                output = output + current_num
    return output


def solve2():
    lines = []
    gears_dict = defaultdict(list)
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.strip())
    for row, line in enumerate(lines):
        current_num = 0
        start_col = -1
        for col, char in enumerate(line):
            if char.isdigit():
                if start_col < 0:
                    start_col = col
                current_num = current_num * 10 + int(char)
            else:
                if start_col >= 0:
                    gears = search_gears(lines, current_num, row, start_col)
                    for gear in gears:
                        gears_dict[f"{gear[0]}-{gear[1]}"].append(current_num)
                current_num = 0
                start_col = -1
        if start_col >= 0:
            gears = search_gears(lines, current_num, row, start_col)
            for gear in gears:
                gears_dict[f"{gear[0]}-{gear[1]}"].append(current_num)

    output = 0
    for key, value in gears_dict.items():
        if len(value) == 2:
            output = output + value[0] * value[1]

    return output


print(f"Q1: {solve1()}")
print(f"Q2: {solve2()}")
