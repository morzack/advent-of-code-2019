get_orbit = lambda x: (x.split(")")[0], x.split(")")[1])
orbits = [get_orbit(i.strip()) for i in open('inputs/day-6.txt').readlines()]

objects = set()
for o in orbits:
    objects.add(o[0])
    objects.add(o[1])

direct_orbits = len(orbits)

indirect_orbits = 0

def get_indirect_orbits(ob_id):
    for i in orbits:
        if i[1] == ob_id:
            a = get_indirect_orbits(i[0])
            a.append(ob_id)
            return a
    return [ob_id]

# for o in objects:
#     indirect_orbits += get_indirect_orbits(o)

# print(indirect_orbits)

start = [i for i in orbits if i[1] == "YOU"][0][0]
end = [i for i in orbits if i[1] == "SAN"][0][0]

start_tree = get_indirect_orbits(start)
end_tree = get_indirect_orbits(end)

pos = 0
for i in start_tree[::-1]:
    following = False
    for j in end_tree:
        if j == i:
            following = True
        if following:
            pos += 1
    if following:
        break
    pos += 1

print(pos-1)