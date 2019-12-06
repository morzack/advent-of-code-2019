orbits = [i.strip().split(")") for i in open('inputs/day-6.txt').readlines()]
orbits = {i[1]: i[0] for i in orbits}

objects = set()
for o in orbits:
    objects.add(o)

def get_indirect_orbits(ob_id):
    orbit_list = []
    parent_body = orbits[ob_id]
    while parent_body != 'COM':
        orbit_list.append(parent_body)
        parent_body = orbits[parent_body]
    return orbit_list[::-1]

print(f"Part 1: {sum([len(get_indirect_orbits(o))+1 for o in objects])}")

start_tree = get_indirect_orbits("YOU")
end_tree = get_indirect_orbits("SAN")

distance = 0
for val, i in enumerate(start_tree[::-1]):
    if i in end_tree:
        distance = len(end_tree)-end_tree.index(i) + val
        break

print(f"Part 2: {distance-1}")