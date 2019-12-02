inputs = [int(i) for i in open("input/day-2.txt", 'r').read().split(",")]
target = 19690720

def run(inputs_initial):
    # we're making a lot of assumptions about behavior here
    # specifically the program will break if the tape pos is bad
    inputs = inputs_initial.copy()
    tape_pos = 0
    while True:
        op = inputs[tape_pos]
        if op == 99:
            break
        a, b, c = inputs[tape_pos+1:tape_pos+4]
        inputs[c] = {
            1: lambda a, b: a + b,
            2: lambda a, b: a * b
        }[op](inputs[a], inputs[b])
        tape_pos += 4
    return inputs

def brute_force(inputs_inital, target, max_input=100):
    # O(n^2) could be improved upon by working backwards
    for a in range(max_input):
        for b in range(max_input):
            inputs = inputs_inital.copy()
            inputs[1:3] = [a, b]
            if run(inputs)[0] == target:
                return a, b
    return -1, -1

inputs_p1 = inputs.copy()
inputs_p1[1:3] = [12, 2]
print(f"part 1: {run(inputs_p1)[0]}")

a, b = brute_force(inputs, target)
print(f"part 2: {100 * a + b}")