

import numpy as np

global tap_positions


def xorLFSR(temp_list1, inp_leng, tap_positions, temp_list2):
    xorLFSR = temp_list1[inp_leng-1]
    for i in range(len(tap_positions)-1):
        xorLFSR = temp_list1[tap_positions[i]] ^ xorLFSR
    temp_list2.append(xorLFSR)
    return temp_list2


def LFSR(bits, tap_positions, inp_data, op_bits):

    tap_positions = [int(i) for i in tap_positions]

    inp_data.insert(0, inp_data[len(inp_data)-1])
    inp_data.pop()

    output = [0]
    inp_leng = len(inp_data)
    temp_list1 = inp_data
    temp_list2 = []
    for i in range(int(op_bits)):
        output.insert(0, temp_list1[inp_leng-1])
        xorLFSR(temp_list1, inp_leng, tap_positions, temp_list2)
        for i in range(inp_leng - 1):
            temp_list2.append(temp_list1[i])

        temp_list1 = temp_list2
        temp_list2 = []

    output.pop()
    output.reverse()
    output_data = ''.join(str(x) for x in output)
    return output_data


bits = np.random.randint(1, 30000)
tap_positions = [np.random.randint(1, 30000)]
inp_data = [1, 0, 1, 0, 1]
inp_data = [int(i) for i in inp_data]
op_bits = input("Number of clock cycles:")
print(inp_data)
print(tap_positions)
print(LFSR(bits, tap_positions, inp_data, op_bits))
