file_path = "data/day1_input.txt"


def solve1():
    sum = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            for ch in line:
                if ch.isdigit():
                    sum += int(ch) * 10
                    break
            for ch in reversed(line):
                if ch.isdigit():
                    sum += int(ch)
                    break
            print(sum)
    return sum


def solve2():
    sum = 0
    digit_hash = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            for idx, ch in enumerate(line):
                if ch.isdigit():
                    sum += int(ch) * 10
                    break
                found = False
                for digit_name, digit in digit_hash.items():
                    if line[idx : idx + len(digit_name)] == digit_name:
                        sum += digit * 10
                        found = True
                        break
                if found:
                    break

            for idx, ch in enumerate(reversed(line)):
                idx = len(line) - idx - 1
                if ch.isdigit():
                    sum += int(ch)
                    break
                found = False
                for digit_name, digit in digit_hash.items():
                    if line[idx : idx + len(digit_name)] == digit_name:
                        sum += digit
                        found = True
                        break
                if found:
                    break
            print(sum)
    return sum


print(f"Q1: {solve1()}")
print(f"Q2: {solve2()}")
