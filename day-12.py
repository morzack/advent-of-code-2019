import re

def read_bodies():
    initial_bodies = []
    with open('inputs/day-12.txt') as f:
        for line in f.readlines():
            split_line = "".join(re.split(r"\D+(?!-*\d+)", line))[1:].split("=")
            positions = [int(i) for i in split_line]
            initial_bodies.append([positions, [0, 0, 0]])
    return initial_bodies
    
def step(bodies):
    for i, moon in enumerate(bodies):
        for j, moon_pair in enumerate(bodies):
            if i != j:
                deltas = [moon[0][x]-moon_pair[0][x] for x in range(3)]
                get_grav = lambda d: -1 if d > 0 else 0 if d == 0 else 1
                for x in range(3):
                    moon[1][x] += get_grav(deltas[x])
    for moon in bodies:
        for i in range(3):
            moon[0][i] += moon[1][i]
    
def get_energy(body):
    pot = sum([abs(i) for i in body[0]])
    kin = sum([abs(i) for i in body[1]])
    return pot * kin

def str_pos(body, index):
    return f"{body[0][index]},{body[1][index]}"

def gcd(a, b):
    r = 1
    l = max(a, b)
    s = min(a, b)
    while r != 0:
        r = l % s
        l = s
        s = r
    return l

def lcm(a, b):
    return (a * b)//gcd(a, b)

p1_bodies = read_bodies()
for i in range(1000):
    step(p1_bodies)
print(f"Part 1: {sum([get_energy(i) for i in p1_bodies])}")

p2_bodies = read_bodies()
repetitions = {"x":set(), "y":set(), "z":set()}
x_rep = y_rep = z_rep = 0
gen = 0
while 0 in {x_rep, y_rep, z_rep}:
    step(p2_bodies)
    hash_index = lambda x: " ".join([str_pos(body, x) for body in p2_bodies])
    if x_rep == 0:
        x_hash = hash_index(0)
        if x_hash in repetitions["x"]:
            x_rep = gen
        else:
            repetitions["x"].add(x_hash)
    if y_rep == 0:
        y_hash = hash_index(1)
        if y_hash in repetitions["y"]:
            y_rep = gen
        else:
            repetitions["y"].add(y_hash)
    if z_rep == 0:
        z_hash = hash_index(2)
        if z_hash in repetitions["z"]:
            z_rep = gen
        else:
            repetitions["z"].add(z_hash)
    gen += 1
print(f"Part 2: {lcm(lcm(x_rep, y_rep), z_rep)}")