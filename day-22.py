def run_instruction(position, instruction, deck_size):
    if instruction.startswith("cut "):
        x = int(instruction[4:])
        return (position - x)
    elif instruction.startswith("deal with increment "):
        x = int(instruction[20:])
        return (position * x)
    elif instruction.startswith("deal into new stack"):
        return -(position + 1)
    return position

def track_position(position, instructions, deck_size):
    for instruction in instructions:
        position = run_instruction(position, instruction, deck_size)
    return position % deck_size

instructions = [i.strip() for i in open('inputs/day-22.txt').readlines()]

# part 1
deck_size = 10007
print(f"Part 1: {track_position(2019, instructions, deck_size)}")

# part 2