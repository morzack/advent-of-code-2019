import math
asteroids = set()
with open("inputs/day-10.txt") as f:
    height = width = 0
    for y, row in enumerate(f.readlines()):
        for x, val in enumerate(row):
            if val == "#":
                asteroids.add((x, y))
            height = y+1
            width = x+1

def get_slope(x1, x2, y1, y2):
    quadrant = 1
    dx = x2-x1
    dy = y2-y1
    if dx >= 0 and dy >= 0:
        quadrant = 1
    elif dx >= 0 and dy < 0:
        quadrant = 4
    elif dx < 0 and dy >= 0:
        quadrant = 2
    elif dx < 0 and dy < 0:
        quadrant = 3
    return dy/dx if dx != 0 else 'INF', quadrant

def get_visible(position):
    slopes = set()
    initial_x, initial_y = position
    for y in range(height):
        for x in range(width):
            if (x, y) in asteroids and not (y == initial_y and x == initial_x):
                slopes.add(get_slope(x, initial_x, y, initial_y))
    return len(slopes)

distances = {asteroid_base: get_visible(asteroid_base) for asteroid_base in asteroids}
max_asteroids = max([i[1] for i in distances.items()])
print(f"Part 1: {max_asteroids}")
station_pos = [i[0] for i in distances.items() if i[1] == max_asteroids][0]

angle_asteroids = []
for asteroid in asteroids:
    dx, dy = station_pos[0] - asteroid[0], station_pos[1] - asteroid[1]
    distance = math.hypot(dx, dy)
    angle = math.degrees(math.atan2(dy, dx))
    angle -= 90
    if angle < 0:
        angle += 360
    angle_asteroids.append((distance, angle, asteroid))

angle_asteroids = sorted(angle_asteroids, key=lambda x: x[0])
angle_asteroids = sorted(angle_asteroids, key=lambda x: x[1])

last_angle = -1
destroyed = 0
index = 0
target_destroyed = 200

while index < len(angle_asteroids):
    asteroid = angle_asteroids[index]
    _, angle, position = asteroid
    if angle != last_angle and len(angle_asteroids) != 1:
        angle_asteroids.remove(asteroid)
        destroyed += 1
        if destroyed == target_destroyed:
            print(f"Part 2: {position[0]*100 + position[1]}")
            break
        last_angle = angle
    else:
        index += 1
    if index >= len(angle_asteroids):
        index = 0