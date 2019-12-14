inputs = open("inputs/day-14.txt").readlines()

def get_reaction(line):
    inputs, outputs = line.strip().split(" => ")
    inputs_array = {}
    outputs_array = {}
    for i in inputs.split(", "):
        num, t = i.split(" ")
        inputs_array[t] = int(num)
    for i in outputs.split(", "):
        num, t = i.split(" ")
        outputs_array[t] = int(num)
    return inputs_array, outputs_array

reactions = [get_reaction(i) for i in inputs]

def get_needed(reactions, t, units):
    for reaction in reactions:
        if t in reaction[1]:
            mats = reaction[0]
            required = {}
            produced = {}
            while produced.get(t, 0) < units:
                for mat in mats:
                    required[mat] = required.get(mat, 0) + mats[mat]
                produced[t] = produced.get(t, 0) + reaction[1][t]
            return required, produced
    return {}, {}

def break_down(reactions, needed):
    next_required = {}
    next_produced = {}
    for need in needed:
        required, produced = get_needed(reactions, need, needed[need])
        for i in required:
            next_required[i] = next_required.get(i, 0) + required[i]
        for i in produced:
            next_produced[i] = next_produced.get(i, 0) + produced[i]
    return next_required, next_produced

def check_only(things, t):
    for thing in things:
        if thing != t and things[thing] > 0:
            return False
    return True

def check_empty(things):
    for thing in things:
        if things[thing] != 0:
            return False
    return True

def get_needed_fuel(surplus={}):
    needed, _ = get_needed(reactions, "FUEL", 1)

    for i in surplus:
        needed[i] = needed.get(i, 0) - surplus[i]

    while not check_only(needed, "ORE"):
        required, produced = break_down(reactions, needed)
        for i in produced:
            needed[i] = needed.get(i, 0) - produced[i]
        for i in required:
            needed[i] = needed.get(i, 0) + required[i]
    return needed["ORE"], {i: abs(needed[i]) for i in needed if needed[i] < 0}

ore_per_fuel, _ = get_needed_fuel()

print(f"Part 1: {ore_per_fuel}")

# in_hold = in_initial = 1000000000000
# fuel = 0
# surplus = {}
# cycle_used = fuel_made = 0
# while in_hold > 0:
#     ore_used, surplus_mats = get_needed_fuel(surplus=surplus)
#     in_hold -= ore_used
#     fuel += 1
#     for i in surplus_mats:
#         surplus[i] = surplus.get(i, 0) + surplus_mats[i]
#     if check_empty(surplus_mats) and check_empty(surplus):
#         cycle_used = in_initial - in_hold
#         fuel_made = fuel
#         break
# print("cycle", fuel_made * (in_initial // cycle_used))