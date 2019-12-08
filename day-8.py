inputs = [int(i) for i in open("inputs/day-8.txt").read()]

width = 6
height = 25
layers = []

pos = 0

while pos < len(inputs):
    building = []
    for x in range(width):
        a = []
        for y in range(height):
            a.append(inputs[pos])
            pos += 1
        building.append(a)
    layers.append(building)

layer_c_s = 0
min_z = -1
for layer_c, layer in enumerate(layers):
    z = 0
    for i in layer:
        for j in i:
            if j == 0:
                z += 1
    if min_z == -1 or z < min_z:
        layer_c_s = layer_c
        min_z = z

ones = 0
twos = 0
for i in layers[layer_c_s]:
    for j in i:
        if j == 1:
            ones += 1
        if j == 2:
            twos += 1

print(ones*twos)

final = {}
for layer in layers:
    for x, row in enumerate(layer):
        for y, col in enumerate(row[::-1]):
            if col != 2:
                if (x, y) not in final:
                    final[(x, y)] = col

for y in range(height):
    for x in range(width):
        print("#" if final[(x, y)] == 1 else " ", end="")
    print("")