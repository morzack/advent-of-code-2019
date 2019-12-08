inputs = [int(i) for i in open("inputs/day-7.txt", 'r').read().split(",")]

class Controller:
    def __init__(self, inputs_initial):
        self.inputs = inputs_initial.copy()
        self.tape_pos = 0
        self.last_output = 0

    def run(self, next_input, break_after_input=False):
        get_in = lambda i, param: self.inputs[i] if param == 0 else i # evaluate and return correct thing based on param
        # get value without using parameter rules
        val = lambda pos: self.inputs[self.tape_pos+1+pos] # 0=a, 1=b, etc
        # get value using parameter rules
        param = lambda pos: get_in(val(pos), int(opcode_raw[2-pos])) # change if more params, 0=a, 1=b, etc
        while True:
            opcode_raw = str(self.inputs[self.tape_pos]).zfill(5)
            op = int(opcode_raw[3:5])
            if op == 99:
                break
            elif op in [3, 4]:
                # 1 param
                if op == 3:
                    self.inputs[val(0)] = next_input
                    self.tape_pos += 2
                    if break_after_input:
                        return None, False
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

def run_phases(controllers, initial):
    out, _ = controllers[0].run(initial)
    for controller in controllers[1:]:
        out, halted = controller.run(out)
    return out, halted

def run_feedback(phase_settings, once=False):
    controllers = [Controller(inputs) for _ in phase_settings]
    for i, controller in enumerate(controllers):
        controller.run(phase_settings[i], True)
    out = 0
    halted = False
    while not halted:
        out, halted = run_phases(controllers, out)
        if once:
            return out
    return out

p1_phases = []
p2_phases = []
for phase in range(00000, 99999):
    s_phase = str(phase).zfill(5)
    phase_chars = []
    valid_1 = True
    valid_2 = True
    for i in s_phase:
        if i in phase_chars:
            valid_1 = valid_2 = False
        elif i not in "01234":
            valid_1 = False
        elif i not in "56789":
            valid_2 = False
        if not valid_1 and not valid_2:
            break
        phase_chars.append(i)
    if valid_1:
        p1_phases.append(run_feedback([int(i) for i in phase_chars], True))
    if valid_2:
        p2_phases.append(run_feedback([int(i) for i in phase_chars]))
print(f"Part 1: {max(p1_phases)}")
print(f"Part 2: {max(p2_phases)}")
