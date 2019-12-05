inputs = [int(i) for i in open("inputs/day-5.txt", 'r').read().split(",")]

def run(inputs_initial):
    inputs = inputs_initial.copy()
    tape_pos = 0
    while True:
        opcode_raw = str(inputs[tape_pos]).zfill(5)
        param_a, param_b, param_c, op = int(opcode_raw[2]), int(opcode_raw[1]), int(opcode_raw[0]), int(opcode_raw[3:5])
        if op == 99:
            break
        elif op in [1, 2]:
            a, b, c = inputs[tape_pos+1:tape_pos+4]
            a_in = inputs[a] if param_a == 0 else a
            b_in = inputs[b] if param_b == 0 else b
            inputs[c] = {
                1: lambda a, b: a + b,
                2: lambda a, b: a * b
            }[op](a_in, b_in)
            tape_pos += 4
        elif op in [3, 4]:
            a = inputs[tape_pos+1]
            if op == 3:
                inputs[a] = int(input("> ").strip())
            elif op == 4:
                print(inputs[a])
            tape_pos += 2
    return inputs


inputs_p1 = inputs.copy()
print(f"part 1: {run(inputs_p1)[0]}")