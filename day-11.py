program = [int(i) for i in open("inputs/day-11.txt").read().split(",")]

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
    
    def step_until_action(self, input_given):
        halted = input_used = output_returned = False
        while not (halted or input_used or output_returned):
            halted, input_used, output_returned = self.step(input_given)
        return halted, input_used, output_returned

def move_robot(pos, rotation):
    pos = pos.copy()
    if rotation == 1:
        pos[2] = 0 if pos[2]+1 > 3 else pos[2]+1
    elif rotation == 0:
        pos[2] = 3 if pos[2]-1 < 0 else pos[2]-1
    dx, dy = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0)
    }[pos[2]]
    pos[0] += dx
    pos[1] += dy
    return pos

get_panel = lambda panels, pos: panels.get((pos[0], pos[1]), 0)

def paint_panel(panels, pos, color):
    panels[(pos[0], pos[1])] = color

def paint_panels(start_color):
    controller = Controller(program)
    panels = {}
    robot_pos = [0, 0, 0] # clock position esque, 0 up ++1 clockwise

    paint_panel(panels, robot_pos[:2], start_color)
    halted = input_used = output_returned = False
    while not halted:
        halted, input_used, output_returned = controller.step_until_action(get_panel(panels, robot_pos[:2]))
        if halted:
            break
        assert input_used

        halted, input_used, output_returned = controller.step_until_action(get_panel(panels, robot_pos[:2]))
        if halted:
            break
        assert output_returned
        color = controller.last_output
        paint_panel(panels, robot_pos[:2], color)
        
        halted, input_used, output_returned = controller.step_until_action(get_panel(panels, robot_pos[:2]))
        if halted:
            break
        assert output_returned
        direction = controller.last_output
        robot_pos = move_robot(robot_pos, direction)
    return panels

print(f"Part 1: {len(paint_panels(0))}")

panels = paint_panels(1)
filled = {i for i in panels if panels[i] == 1}

filled = sorted(filled, key=lambda x: x[0])
min_x, max_x = filled[0][0], filled[-1][0]

filled = sorted(filled, key=lambda x: x[1])
min_y, max_y = filled[0][1], filled[-1][1]

board = [[0 for _ in range(max_x-min_x+1)] for _ in range(max_y-min_y+1)]
for panel in filled:
    board[panel[1]-min_y][panel[0]-min_x] = 1

board = board[::-1]
print("Part 2:")
print("\n".join(["".join(["█" if col == 1 else " " for col in row]) for row in board]))