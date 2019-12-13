program = [int(i) for i in open("inputs/day-13.txt").read().split(",")]

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

controller = Controller(program)
controller.tape[0] = 2

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

def get_tile(tiles, x, y):
    return tiles.get((x, y), EMPTY)

def set_tile(tiles, x, y, tile):
    tiles[(x, y)] = tile
    return tiles

def get_tile_pos(tiles, tile_type):
    for pos in tiles:
        if tiles[pos] == tile_type:
            return pos
    return (-1, -1)

def get_paddle_dir(tiles):
    paddle_pos = get_tile_pos(tiles, PADDLE)
    ball_pos = get_tile_pos(tiles, BALL)
    return -1 if paddle_pos[0] > ball_pos[0] else 0 if paddle_pos[0] == ball_pos[0] else 1

def get_outputs(controller, tiles, i=-2):
    outputs = []
    score = 0
    input_used = halted = False
    while not (input_used or halted):
        halted, input_used, output_sent = controller.step_until_action(get_paddle_dir(tiles) if i == -2 else i)
        outputs.append(controller.last_output)
        if len(outputs) == 3:
            x, y, tile = outputs
            if x == -1 and y == 0:
                score = tile
            tiles = set_tile(tiles, x, y, tile)
            outputs = []
    return tiles, score, halted, input_used, output_sent
tiles, score, halted, _, _ = get_outputs(controller, {}, i=0)

def count_tiles(tiles, tile_type):
    blocks = 0
    for pos in tiles:
        if tiles[pos] == tile_type:
            blocks += 1
    return blocks

def render_tiles(tiles):
    for y in range(23):
        s = ""
        for x in range(42):
            s += {
                EMPTY: " ",
                WALL: "█",
                BLOCK: "#",
                PADDLE: "-",
                BALL: "o"
            }[get_tile(tiles, x, y)]
        print(s)

print(f"Part 1: {count_tiles(tiles, BLOCK)}")

rendering = False
if rendering:
    import os, time

while not halted:
    new_tiles, score, halted, _, _ = get_outputs(controller, tiles)

    for tile in new_tiles:
        tiles = set_tile(tiles, tile[0], tile[1], new_tiles[tile])

    if rendering:
        os.system("clear")
        render_tiles(tiles)
        print(score)
        time.sleep(0.01)

print(f"Part 2: {score}")