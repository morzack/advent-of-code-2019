inputs = [int(i) for i in open("inputs/day-7.txt", 'r').read().split(",")]

class controller:
    def __init__(self, inputs_initial):
        self.inputs = inputs_initial.copy()
        self.tape_pos = 0
        self.opcode_raw = ""
        self.last_output = 0

    def run(self, next_input, break_after_input=False):
        get_in = lambda i, param: self.inputs[i] if param == 0 else i # evaluate and return correct thing based on param
        # get value without using parameter rules
        val = lambda pos: self.inputs[self.tape_pos+1+pos] # 0=a, 1=b, etc
        # get value using parameter rules
        param = lambda pos: get_in(val(pos), int(self.opcode_raw[2-pos])) # change if more params, 0=a, 1=b, etc
        while True:
            self.opcode_raw = str(self.inputs[self.tape_pos]).zfill(5)
            op = int(self.opcode_raw[3:5])
            if op == 99:
                break
            elif op in [3, 4]:
                # 1 param
                if op == 3:
                    self.inputs[val(0)] = next_input
                    self.tape_pos += 2
                    if break_after_input:
                        return
                elif op == 4:
                    self.last_output = param(0)
                    self.tape_pos += 2
                    return self.last_output, False
            elif op in [5, 6]:
                # 2 params
                self.tape_pos = {
                    5: param(1) if param(0) != 0 else self.tape_pos+3,
                    6: param(1) if param(0) == 0 else self.tape_pos+3
                }[op]
            elif op in [1, 2, 7, 8]:
                self.inputs[val(2)] = {
                    1: lambda a, b: a + b,
                    2: lambda a, b: a * b,
                    7: lambda a, b: 1 if a < b else 0,
                    8: lambda a, b: 1 if a == b else 0
                }[op](param(0), param(1))
                self.tape_pos += 4
        return self.last_output, True

def run_controller(inputs, phase, previous):
    inputs_p = inputs.copy()
    final_state = run(inputs_p, [phase, previous])
    return final_state

def run_phases(c_a, c_b, c_c, c_d, c_e, initial):
    a, h = c_a.run(initial)
    b, h = c_b.run(a)
    c, h = c_c.run(b)
    d, h = c_d.run(c)
    e, halted = c_e.run(d)
    return e, halted

def run_feedback(phase_settings):
    c_a = controller(inputs)
    c_a.run(phase_settings[0], True)
    c_b = controller(inputs)
    c_b.run(phase_settings[1], True)
    c_c = controller(inputs)
    c_c.run(phase_settings[2], True)
    c_d = controller(inputs)
    c_d.run(phase_settings[3], True)
    c_e = controller(inputs)
    c_e.run(phase_settings[4], True)

    out = 0
    halted = False
    while not halted:
        out, halted = run_phases(c_a, c_b, c_c, c_d, c_e, out)
    return out

phases = []
for phase in range(00000, 99999):
    s_phase = str(phase).zfill(5)
    phase_chars = []
    valid = True
    for i in s_phase:
        if i in phase_chars or i not in "56789":
            valid = False
        phase_chars.append(i)
    if valid:
        phases.append(run_feedback([int(i) for i in phase_chars]))
print(max(phases))
