program = [int(i) for i in open("inputs/day-9.txt").read().split(",")]

class Controller:
    def __init__(self, inputs):
        self.tape = {}
        for i, val in enumerate(inputs):
            self.tape[i] = val
        self.tape_pos = 0
        self.relative_pos = 0
        self.last_output = 0
    
    def get_tape(self, i):
        return self.tape.get(i, 0)
    
    def get_val(self, mode, index):
        assert mode in [0, 1, 2]
        if mode == 0:
            return self.get_tape(self.get_tape(index))
        elif mode == 1:
            return self.get_tape(index)
        elif mode == 2:
            return self.get_tape(self.get_tape(index) + self.relative_pos)

    def write_val(self, mode, index, val):
        assert mode in [0, 2]
        if mode == 0:
            self.tape[self.get_tape(index)] = val
        elif mode == 2:
            self.tape[self.get_tape(index) + self.relative_pos] = val

    def step(self, next_input):
        # return bools for (halted, input_used, output_returned)
        opcode_raw = str(self.get_tape(self.tape_pos)).zfill(5)
        op = int(opcode_raw[3:5])
        opcode_c, opcode_b, opcode_a = [int(i) for i in opcode_raw[:3]]
        tape_a, tape_b, tape_c = [self.tape_pos+i+1 for i in range(3)]
        
        assert op in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]
        
        if op == 99:
            return True, False, False
        elif op in [3, 4, 9]:
            # 1 param
            if op == 3:
                self.write_val(opcode_a, tape_a, next_input)
                self.tape_pos += 2
                return False, True, False
            elif op == 4:
                self.last_output = self.get_val(opcode_a, tape_a)
                self.tape_pos += 2
                return False, False, True
            elif op == 9:
                self.relative_pos += self.get_val(opcode_a, tape_a)
                self.tape_pos += 2
        elif op in [5, 6]:
            # 2 params
            self.tape_pos = {
                5: self.get_val(opcode_b, tape_b) if self.get_val(opcode_a, tape_a) != 0 else self.tape_pos+3,
                6: self.get_val(opcode_b, tape_b) if self.get_val(opcode_a, tape_a) == 0 else self.tape_pos+3
            }[op]
        elif op in [1, 2, 7, 8]:
            self.write_val(opcode_c, tape_c, {
                1: lambda a, b: a + b,
                2: lambda a, b: a * b,
                7: lambda a, b: 1 if a < b else 0,
                8: lambda a, b: 1 if a == b else 0
            }[op](self.get_val(opcode_a, tape_a), self.get_val(opcode_b, tape_b)))
            self.tape_pos += 4
        return False, False, False

def run_controller_inputs(program, inputs):
    controller = Controller(program)
    next_input = 0
    halted = input_used = output_returned = False
    outputs = []
    while not halted:
        halted, input_used, output_returned = controller.step(inputs[next_input])
        if input_used and input_used < len(inputs)-2:
            next_input += 1
        if output_returned:
            outputs.append(controller.last_output)
    return outputs

print(f"Part 1: {run_controller_inputs(program, [1])[0]}")
print(f"Part 2: {run_controller_inputs(program, [2])[0]}")