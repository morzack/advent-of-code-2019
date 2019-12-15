from intcode import Controller, load_program
import random
import os
import sys
sys.setrecursionlimit(1000)

controller = Controller(load_program("inputs/day-15.txt"))

directions = {
    "N": 1,
    "S": 2,
    "W": 3,
    "E": 4
}

status = {
    0: "#",
    1: ".",
    2: "O"
}

pos = (0, 0)
tiles = {pos: "."}

def update_robot(direction, status):
    global pos
    dx, dy = {
        1: (0, 1),
        2: (0, -1),
        3: (-1, 0),
        4: (1, 0)
    }[direction]
    
    temp_x = pos[0] + dx
    temp_y = pos[1] + dy

    if status == 0:
        tiles[(temp_x, temp_y)] = "#"
    elif status == 1:
        tiles[(temp_x, temp_y)] = "."
        pos = (temp_x, temp_y)
    elif status == 2:
        tiles[(temp_x, temp_y)] = "O"
        pos = (temp_x, temp_y)

last_dir = 1
def update_dir(status):
    global last_dir
    last_dir = random.choice([1, 2, 3, 4])

def check_filled(tiles):
    for i in tiles:
        if tiles[i] == ".":
            x, y = i
            if (x+1, y) not in tiles:
                return False
            if (x-1, y) not in tiles:
                return False
            if (x, y+1) not in tiles:
                return False
            if (x, y-1) not in tiles:
                return False
    return True

def render_tiles(tiles, pos):
    min_x = min_y = max_x = max_y = 0
    for tile in tiles:
        x, y = tile
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    for y in range(min_y, max_y+1):
        s = ""
        for x in range(min_x, max_x+1):
            if (x, y) == (0, 0):
                s += "X"
            elif (x, y) == pos:
                s += "@"
            else:
                s += tiles.get((x, y), " ")
        print(s)

# halted = input_used = output_returned = False
# input_giving = 0
# while not check_filled(tiles):
#     halted, input_used, output_returned = controller.step_until_action(last_dir)
#     if output_returned:
#         update_robot(last_dir, controller.last_output)
#         update_dir(controller.last_output)
#         # if controller.last_output == 2:
#             # break
#         # render_tiles(tiles, pos)
        # os.system("clear")

with open("inputs/day-15-map.txt") as f:
    rows = f.readlines()
    tiles = {}
    for y, row in enumerate(rows):
        for x, col in enumerate(row.replace("\n", "")):
            if col == "O":
                end_pos = (x, y)
            if col == "X":
                tiles[(x, y)] = "."
                starting_pos = (x, y)
            else:
                tiles[(x, y)] = col

render_tiles(tiles, pos)

def traverse(start, end, tiles, nodes=-1, traversed=set()):
    if nodes == -1:
        nodes = {}
        for i in tiles:
            if tiles[i] == ".":
                x, y = i
                available = []
                if tiles.get((x+1, y), " ") in ".O":
                    available.append((x+1, y))
                if tiles.get((x-1, y), " ") in ".O":
                    available.append((x-1, y))
                if tiles.get((x, y+1), " ") in ".O":
                    available.append((x, y+1))
                if tiles.get((x, y-1), " ") in ".O":
                    available.append((x, y-1))
                nodes[i] = available
    if start == end:
        return 1
    adjacent = nodes[start]
    min_distance = -1
    for node in nodes[start]:
        if node not in traversed:
            traversed.add(node)
            distance = traverse(node, end, tiles, nodes.copy(), traversed.copy())
            if distance != 0:
                if min_distance == -1:
                    min_distance = distance
                if distance < min_distance:
                    min_distance = distance
    return min_distance + 1

print(f"Part 1: {traverse(starting_pos, end_pos, tiles.copy())-1}")
# this is cursed -- it's the same as the previous line but returns something different !?a
print(f"Part 1: {traverse(starting_pos, end_pos, tiles.copy())-1}")

# part 2 is getting the longest node back to the start
distances = set()
for tile in tiles:
    if tiles[tile] in ".OX":
        distances.add(traverse(tile, end_pos, tiles.copy()))
print(f"Part 2: {max(distances)-1}")