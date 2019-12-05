inputs = [int(i) for i in open("inputs/day-5.txt", 'r').read().split(",")]

def run(inputs_initial):
    inputs = inputs_initial.copy()
    tape_pos = 0
    opcode_raw = ""
    get_in = lambda i, param: inputs[i] if param == 0 else i # evaluate and return correct thing based on param
    # get value without using parameter rules
    val = lambda pos: inputs[tape_pos+1+pos] # 0=a, 1=b, etc
    # get value using parameter rules
    param = lambda pos: get_in(val(pos), int(opcode_raw[2-pos])) # change if more params, 0=a, 1=b, etc
    while True:
        opcode_raw = str(inputs[tape_pos]).zfill(5)
        op = int(opcode_raw[3:5])
        if op == 99:
            break
        elif op in [3, 4]:
            # 1 param
            if op == 3:
                inputs[val(0)] = int(input("> "))
            elif op == 4:
                print(param(0))
            tape_pos += 2
        elif op in [5, 6]:
            # 2 params
            tape_pos = {
                5: param(1) if param(0) != 0 else tape_pos+3,
                6: param(1) if param(0) == 0 else tape_pos+3
            }[op]
        elif op in [1, 2, 7, 8]:
            inputs[val(2)] = {
                1: lambda a, b: a + b,
                2: lambda a, b: a * b,
                7: lambda a, b: 1 if a < b else 0,
                8: lambda a, b: 1 if a == b else 0
            }[op](param(0), param(1))
            tape_pos += 4
    return inputs

inputs_p1 = inputs.copy()
final_state = run(inputs_p1)