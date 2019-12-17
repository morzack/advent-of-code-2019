inputs = [int(i) for i in open("inputs/day-16.txt").read().strip()]
inputs *= 10000
offset = int("".join([str(i) for i in inputs[:7]]))
def apply_phase(inputs):
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

print_inputs = lambda x: "".join(str(i) for i in x)

for phase in range(100):
    inputs = apply_phase(inputs)

print(print_inputs(inputs[offset:offset+8]))