def check_valid(i):
    char_counts = {}
    previous_val = 0
    for char in i:
        char_counts[char] = char_counts.get(char, 0) + 1
        if ord(char) < previous_val:
            return False, False
        previous_val = ord(char)
    part_1 = len([j for j in [char_counts[i] for i in char_counts] if j >= 2])
    part_2 = 2 in [char_counts[i] for i in char_counts]
    return part_1, part_2

input_range = open('inputs/day-4.txt').read().split("-")
valid_1, valid_2 = [len([i for i in range(int(input_range[0]), int(input_range[1])) if check_valid(str(i))[n]]) for n in [0, 1]]

print(f"Part 1: {valid_1}")
print(f"Part 2: {valid_2}")