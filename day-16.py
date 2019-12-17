inputs = [int(i) for i in open("inputs/day-16.txt").read().strip()]

def apply_phase_part_1(inputs):
    # Naiive solution
    pattern = [0, 1, 0, -1]
    out = []
    for repeating, _ in enumerate(inputs):
        s = 0
        index = 0
        r = 0
        for val in inputs:
            r += 1
            if r > (repeating):
                index += 1
                r = 0
            if index >= 4:
                index = 0
            s += (val * pattern[int(index)])
        out.append(abs(s) % 10)
    return out

def apply_phase_part_2(inputs, offset, times=100):
    # new and improved solution
    inputs *= 10000
    inputs = inputs[offset:]
    for _ in range(times):
        s = 0
        for i, val in enumerate(inputs[::-1]):
            s = (val + s) % 10
            inputs[len(inputs)-i-1] = s
    return inputs[:8]

print_inputs = lambda x: "".join(str(i) for i in x)

inputs_p1 = inputs.copy()
for _ in range(100):
    inputs_p1 = apply_phase_part_1(inputs_p1)
print(f"Part 1: {print_inputs(inputs_p1)[:8]}")

offset = int("".join([str(i) for i in inputs[:7]]))
print(f"Part 2: {print_inputs(apply_phase_part_2(inputs.copy(), offset))}")
