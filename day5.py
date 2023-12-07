from collections import defaultdict

file_path = "data/day5_input.txt"


class SoruceDestRange:
    def __init__(self, dest_range_start, source_range_start, range_len):
        self.dest_range_start = int(dest_range_start)
        self.source_range_start = int(source_range_start)
        self.range_len = int(range_len)

    def convert(self, num):
        num = int(num)
        if (
            self.source_range_start <= num
            and num < self.source_range_start + self.range_len
        ):
            return self.dest_range_start + num - self.source_range_start

        return -1


def solve1():
    output = -1
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.strip())

    seeds = lines[0].split()[1:]
    for seed in seeds:
        curr = seed
        mapped = -1
        for line in lines[2:]:
            nums = line.split()
            if len(nums) == 0:
                if mapped == -1:
                    mapped = curr
                curr = mapped
                mapped = -1
            if len(nums) == 0 or not nums[0].isdigit():
                continue
            if mapped != -1:
                continue
            r = SoruceDestRange(nums[0], nums[1], nums[2])
            if mapped == -1:
                mapped = r.convert(curr)
            else:
                mapped = r.convert(mapped)
        if mapped != -1:
            curr = mapped
        if output == -1:
            output = curr
        else:
            output = min(curr, output)

    return output


print(f"Q1: {solve1()}")
