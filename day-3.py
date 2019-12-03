wire_details = open("inputs/day-3.txt").readlines()

calc_distance = lambda x: abs(int(x.split(" ")[0])) + abs(int(x.split(" ")[1]))

update_pos = lambda x, y, direction: {
    "R": lambda x, y: [x+1, y],
    "L": lambda x, y: [x-1, y],
    "U": lambda x, y: [x, y+1],
    "D": lambda x, y: [x, y-1]
}[direction](x, y)

def build_wire(wire_detail):
    x, y = 0, 0
    wire = set()
    for instruction in wire_detail.split(","):
        direction, length = instruction[0], int(instruction[1:])
        for _ in range(length):
            x, y = update_pos(x, y, direction)
            wire.add(f"{x} {y}")
    return wire

wire_a, wire_b = [build_wire(wire_detail) for wire_detail in wire_details]
intersected = wire_a.intersection(wire_b)
print(f"Part 1: {min(map(calc_distance, intersected))}")

def track_wire(wire_detail, point_of_interest):
    # see how long to hit point of interest
    distance = 1
    x, y = 0, 0
    passed = {}
    for instruction in wire_detail.split(","):
        direction, length = instruction[0], int(instruction[1:])
        for _ in range(length):
            x, y = update_pos(x, y, direction)
            pos = f"{x} {y}"
            if pos == point_of_interest:
                return distance
            if pos in passed and passed[pos] > distance or pos not in passed:
                passed[pos] = distance
            distance += 1
    return -1

distances = [sum([track_wire(wire, candidate) for wire in wire_details]) for candidate in intersected]
print(f"Part 2: {min(distances)}")