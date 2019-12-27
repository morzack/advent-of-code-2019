from intcode import Controller, load_program

def build_network(controller_count=50):
    network = {}
    for i in range(controller_count):
        network[i] = Controller(load_program("inputs/day-23.txt"))
    reset_network(network)
    return network

def step_network(network, packets_building, packet_queue):
    device_ops = {i: (False, False, False) for i in network}
    # build packets and update queue
    packets_built = set()
    for i in packets_building:
        if len(packets_building[i]) == 3:
            address, x, y = packets_building[i][0:3]
            packets_building[i] = []
            packet_queue[address].extend([x, y])
            packets_built.add((address, x, y))

    # step all the machines
    for device_id in network:
        next_input = -1 if len(packet_queue[device_id]) == 0 else packet_queue[device_id][0]
        halted, input_used, output_returned = network[device_id].step(next_input)
        assert not halted
        if input_used and next_input != -1:
            packet_queue[device_id].pop(0)
            device_ops[device_id] = (True, False, False)
        if input_used and next_input == -1:
            device_ops[device_id] = (False, False, True)
        if output_returned:
            packets_building[device_id].append(network[device_id].last_output)
            device_ops[device_id] = (False, True, False)
    return packets_built, device_ops

def gen_network_dict(network):
    d = {i: [] for i in network}
    d[255] = []
    return d

def check_idle(packets_building, packets_queue, packets_built, device_actions):
    for device_id in packets_building:
        if len(packets_building[device_id]) != 0 or len(packets_queue[device_id]) != 0 and device_id != 255:
            return False
    for device_id in device_actions:
        read, write, failed_read = device_actions[device_id]
        if read or write:
            return False
    return len(packets_built) == 0

def reset_network(network):
    for machine_id in network:
        network[machine_id].reset()
        _, input_used, _ = network[machine_id].step_until_action(machine_id)
        assert input_used

def run_network(network, part_1=False):
    reset_network(network)
    packets_building = gen_network_dict(network)
    packet_queue = gen_network_dict(network)
    nat_packets = []
    last_delivered_nat = ()
    last_device_actions = {i: (True, False, False) for i in network}
    while True:
        packets_built, device_ops = step_network(network, packets_building, packet_queue)
        for packet in packets_built:
            if packet[0] == 255:
                # send it to the NAT
                nat_packets.append(packet)
                if part_1:
                    return packet[2]
        for device_id in device_ops:
            read, write, failed_read = device_ops[device_id]
            if read or write or failed_read:
                last_device_actions[device_id] = (read, write, failed_read)
        if check_idle(packets_building, packet_queue, packets_built, last_device_actions) and len(nat_packets) > 0:
            if not part_1:
                if len(nat_packets) >= 2 and nat_packets[-1][2] == last_delivered_nat[2]:
                    return nat_packets[-1][2]
            last_delivered_nat = nat_packets[-1]
            packet_queue[0].extend(nat_packets[-1][1:3])

network = build_network()
print(f"Part 1: {run_network(network, part_1=True)}")
print(f"Part 2: {run_network(network)}")