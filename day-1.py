calc_fuel = lambda x: x // 3 - 2

def full_calc(mass):
    masses = [mass]
    while (mass := calc_fuel(masses[-1])) > 0:
        masses.append(mass)
    return sum(masses[1:])

inputs = open('inputs/day-1.txt', 'r').readlines()
print(sum([calc_fuel(int(x)) for x in inputs]))
print(sum([full_calc(int(x)) for x in inputs]))