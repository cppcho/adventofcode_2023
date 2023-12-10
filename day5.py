import collections
import unittest
import re

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


# ---------------------------------------------


class InputRange:
    def __init__(self, start, length):
        self.start = int(start)
        self.length = int(length)
        self.end = int(start) + int(length) - 1

    def __repr__(self):
        return f"InputRange: [{self.start}, {self.end}]"

    def __eq__(self, other):
        return self.start == other.start and self.length == other.length


class MappingRange:
    def __init__(self, dest_start, src_start, length):
        self.dest_start = int(dest_start)
        self.src_start = int(src_start)
        self.length = int(length)
        self.src_end = int(src_start) + int(length) - 1
        self.dest_end = int(dest_start) + int(length) - 1

    def __repr__(self):
        return f"MappingRange: [{self.src_start}, {self.src_end}] -> [{self.dest_start}, {self.dest_end}]"


class MappingLayer:
    def __init__(self):
        self.mapping_ranges = []

    def __repr__(self):
        return str.format("MappingLayer: {}", self.mapping_ranges)

    def append(self, mapping_range):
        assert isinstance(mapping_range, MappingRange)
        self.mapping_ranges.append(mapping_range)

    # convert input_range to output range through the mapping layer
    def convert(self, input_range):
        output = []
        input_ranges = [input_range]
        for mapping_range in self.mapping_ranges:
            next_input_ranges = []
            for input_range in input_ranges:
                # if input_range falls out of the mapping range
                if (
                    input_range.end < mapping_range.src_start
                    or mapping_range.src_end < input_range.start
                ):
                    # Go next
                    next_input_ranges.append(input_range)
                    continue

                # if input range lies completely within the mapping src range
                if (
                    mapping_range.src_start <= input_range.start
                    and input_range.end <= mapping_range.src_end
                ):
                    output.append(
                        InputRange(
                            start=mapping_range.dest_start
                            + input_range.start
                            - mapping_range.src_start,
                            length=input_range.length,
                        )
                    )
                # if input range cover completely the mapping src range
                elif (
                    input_range.start < mapping_range.src_start
                    and input_range.end > mapping_range.src_end
                ):
                    output.append(
                        InputRange(
                            start=mapping_range.dest_start,
                            length=mapping_range.length,
                        )
                    )
                    next_input_ranges.append(
                        InputRange(
                            start=input_range.start,
                            length=mapping_range.src_start - input_range.start,
                        )
                    )
                    next_input_ranges.append(
                        InputRange(
                            start=mapping_range.src_end + 1,
                            length=input_range.end - mapping_range.src_end,
                        )
                    )

                # if input range lies partially within the mapping src range(left side)
                elif (
                    input_range.start < mapping_range.src_start
                    and input_range.end >= mapping_range.src_start
                ):
                    output.append(
                        InputRange(
                            start=mapping_range.dest_start,
                            length=input_range.start
                            + input_range.length
                            - mapping_range.src_start,
                        )
                    )
                    next_input_ranges.append(
                        InputRange(
                            start=input_range.start,
                            length=mapping_range.src_start - input_range.start,
                        )
                    )

                # if input range lies partially within the mapping src range(right side)
                elif (
                    input_range.start >= mapping_range.src_start
                    and input_range.start + input_range.length
                    > mapping_range.src_start + mapping_range.length
                ):
                    output.append(
                        InputRange(
                            start=mapping_range.dest_start
                            + input_range.start
                            - mapping_range.src_start,
                            length=mapping_range.src_end - input_range.start + 1,
                        )
                    )
                    next_input_ranges.append(
                        InputRange(
                            start=mapping_range.src_end + 1,
                            length=input_range.end - mapping_range.src_end,
                        )
                    )

            input_ranges = next_input_ranges

        output.extend(next_input_ranges)
        return output


def parse():
    lines = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.strip())

    matches = re.findall(r"\d+", lines[0])
    input_ranges = [
        InputRange(start=a, length=b) for (a, b) in zip(matches[::2], matches[1::2])
    ]
    mapping_layers = []

    new_layer = True
    for line in lines[1:]:
        matches = re.findall(r"\d+", line)
        if len(matches) != 3:
            new_layer = True
            continue

        if new_layer:
            mapping_layers.append(MappingLayer())
            new_layer = False

        mapping_layers[-1].append(MappingRange(*matches))

    return (input_ranges, mapping_layers)


def solve2():
    # input = list of ranges
    # layer1,2,3,4,5 of mappings
    input_ranges, mapping_layers = parse()

    for mapping_layer in mapping_layers:
        output_ranges = []

        for input_range in input_ranges:
            converted = mapping_layer.convert(input_range)
            for c in converted:
                output_ranges.append(c)

        input_ranges = output_ranges

    return min(r.start for r in input_ranges)


class TestConverter(unittest.TestCase):
    def test_convert(self):
        layer = MappingLayer()
        layer.append(MappingRange(11, 21, 10))

        self.assertListEqual(layer.convert(InputRange(22, 9)), [InputRange(12, 9)])
        self.assertListEqual(
            layer.convert(InputRange(20, 30)),
            [InputRange(11, 10), InputRange(20, 1), InputRange(31, 19)],
        )
        self.assertListEqual(
            layer.convert(InputRange(19, 9)), [InputRange(11, 7), InputRange(19, 2)]
        )
        self.assertListEqual(
            layer.convert(InputRange(28, 9)), [InputRange(18, 3), InputRange(31, 6)]
        )

        self.assertListEqual(layer.convert(InputRange(1, 19)), [InputRange(1, 19)])
        self.assertListEqual(layer.convert(InputRange(31, 10)), [InputRange(31, 10)])


print(f"Q1: {solve1()}")
print(f"Q2: {solve2()}")

# unittest.main()
