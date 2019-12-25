from intcode import Controller, load_program

def read_ascii_controller(controller, next_input=0):
    outputs = []
    halted = input_used = output_returned = False
    while not halted and not input_used:
        halted, input_used, output_returned = controller.step_until_action(next_input)
        if output_returned:
            try:
                outputs.append(chr(controller.last_output))
            except ValueError:
                outputs.append(str(controller.last_output))
    return outputs

def write_springscript(controller, program):
    program_str = "\n".join(program) + "\n"
    inputs = [ord(i) for i in program_str]
    halted = input_used = output_returned = False
    current_char = 0
    while current_char < len(program_str):
        halted, input_used, output_returned = controller.step_until_action(inputs[current_char])
        assert not halted
        if input_used:
            current_char += 1

def run_springscript(controller, program):
    controller.reset()
    write_springscript(controller, program)
    ascii_output = read_ascii_controller(controller)
    return "".join(ascii_output)

controller = Controller(load_program("inputs/day-21.txt"))

# part 1 rules:
# if there's a hole either in front or two spaces in front of me and ground 4 spaces away, then jump
print("Part 1: " + run_springscript(controller, [
    "NOT C J",
    "NOT A T",
    "OR T J",
    "AND D J",
    "WALK"
]))

# part 2 rules:
# 
print("Part 2: " + run_springscript(controller, [
    "NOT C J",
    "NOT B T",
    "OR T J",
    "NOT A T",
    "OR T J",
    "AND D J",
    "NOT E T",
    "NOT T T",
    "OR H T",
    "AND T J",
    "RUN"    
]))