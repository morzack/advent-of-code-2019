# DISCLAIMER:
# This is slow. Like _really_ slow.
# Don't run it unless you have an hour to burn
# The cause of the slowness is in the way that the reactions are handled:
# I implemented them _sequentially_ meaning that it turns into an O(n^2) type problem
# Which is Bad.
# I might come back and fix this, idk

import math, time

def get_reaction(line):
    inputs, outputs = line.strip().split(" => ")
    inputs_needed = {}
    for i in inputs.split(", "):
        num, t = i.split(" ")
        inputs_needed[t] = int(num)
    outputs_produced = {outputs.split(" ")[1]: int(outputs.split(" ")[0])}
    return inputs_needed, outputs_produced

def run_reaction(reactions, t, units, initial_resources):
    pool = initial_resources
    consumed = {}
    produced = {}
    for reaction in reactions:
        if t in reaction[1]:
            while produced.get(t, 0) < units:
                for reactant in reaction[0]:
                    used = reaction[0][reactant]
                    if reactant in pool:
                        if used <= pool[reactant]:
                            pool[reactant] -= used
                            used = 0
                        else:
                            used = used - pool[reactant]
                            pool[reactant] = 0
                    consumed[reactant] = consumed.get(reactant, 0) + used
                produced[t] = produced.get(t, 0) + reaction[1][t]
            break
    return pool, consumed, produced

def break_down(reactions, required_resources, initial_resources):
    pool = initial_resources
    consumed = {}
    produced = {}
    for resource in required_resources:
        pool, consumed_step, produced_step = run_reaction(reactions, resource, required_resources[resource], pool)
        for i in consumed_step:
            consumed[i] = consumed.get(i, 0) + consumed_step[i]
        for i in produced_step:
            produced[i] = produced.get(i, 0) + produced_step[i]
    return pool, consumed, produced

def check_only(resources, t):
    for resource in resources:
        if resource != t and resources[resource] > 0:
            return False
    return True

def check_empty(resources):
    for resource in resources:
        if resources[resource] != 0:
            return False
    return True

def get_required_fuel(reactions, pool={}):
    pool, consumed, _ = run_reaction(reactions, "FUEL", 1, pool)
    
    while not check_only(consumed, "ORE"):
        pool, consumed_step, produced_step = break_down(reactions, consumed, pool)
        for i in consumed_step:
            consumed[i] = consumed.get(i, 0) + consumed_step[i]
        for i in produced_step:
            consumed[i] = consumed.get(i, 0) - produced_step[i]
            if consumed[i] < 0:
                pool[i] = abs(consumed[i])
                consumed[i] = 0
    
    return consumed["ORE"], pool

def produce_fuel(reactions, amount):
    # in retrospect the key issue with my program is here and how it takes ages to compute this
    # it should be parallellized if possible
    pool = {}
    ore_used = 0
    for _ in range(amount):
        ore_step, pool = get_required_fuel(reactions, pool)
        ore_used += ore_step
    return ore_used

recipies = [get_reaction(i) for i in open("inputs/day-14.txt").readlines()]

ore_per_fuel = produce_fuel(recipies, 1)
print(f"Part 1: {ore_per_fuel}")

ore_goal = 1000000000000

# linear interpolation :P
# x = fuel wanted
# y = ore used
x1 = 10000
x2 = 1000000
y1 = produce_fuel(recipies, x1)
y2 = produce_fuel(recipies, x2)
slope = (y2-y1) / (x2-x1)
slope = 1/slope
print(f"Part 2: {round(slope*ore_goal)}")

# here's a pretty bad binary search implementation
# fuel_guess = 1
# min_fuel = max_fuel = 0
# # basically find the bounds for the ore used to reach the goal
# while True:
#     ore_used = produce_fuel(recipies, fuel_guess)
#     if ore_used > ore_goal:
#         break
#     min_fuel = fuel_guess
#     fuel_guess *= 2
#     max_fuel = fuel_guess
#     print(f"{ore_used/ore_goal * 100}% complete")
# while max_fuel - min_fuel > 1:
#     # minimize the difference between the two to get the true value
#     print(max_fuel-min_fuel, min_fuel, max_fuel)
#     mid = (max_fuel+min_fuel)//2
#     ore_used = produce_fuel(recipies, mid)
#     if ore_used > ore_goal:
#         max_fuel = mid
#     else:
#         min_fuel = mid
# print(min_fuel)