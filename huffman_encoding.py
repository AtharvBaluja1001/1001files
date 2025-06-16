import sys

def generate_codes(node, current_code):
    global code_dict

    if node[2] == None:
        character = node[1]
        code_dict[character] = current_code
        return
    
    left_child = node[2][0]
    right_child = node[2][1]

    generate_codes(left_child, current_code + "0")
    generate_codes(right_child, current_code + "1")

def make_file(content_bits, code_dict, output_path):
    total_bits = len(content_bits)
    print(total_bits)

    pad_length = (8 - (total_bits % 8)) % 8
    padded_bitstring = content_bits + pad_length * '0'

    byte_list = bytearray()
    for i in range(0, len(padded_bitstring), 8):
        byte = padded_bitstring[i:i+8]
        byte_list.append(int(byte, 2))
    
    with open(output_path, "wb") as file:
        file.write(total_bits.to_bytes(4, byteorder='little'))

        for symbol, code in code_dict.items():
            file.write(bytes([symbol]))
            file.write(len(code).to_bytes(1, 'little'))
            file.write(int(code, 2).to_bytes((len(code)+7)//8, 'big'))

        file.write(b'\n\n\n')

        file.write(byte_list)

if __name__ == "__main__":
    args = sys.argv
    file_path = args[1]
    output_path = args[2]
    
    if ".txt" in file_path:
        with open(file_path, "r") as file:
            content = file.read()
    else:
        with open(file_path, "rb") as file:
            content = file.read()
    
    frequency_table = {}

    for byte in content:
        if byte in frequency_table:
            frequency_table[byte] += 1
        else:
            frequency_table[byte] = 1
    
    initial_list = []

    for byte in frequency_table:
        initial_list.append([frequency_table[byte], byte, None])
    
    initial_list.sort()
    final_list = initial_list

    while len(final_list) > 1:
        left = final_list[0]
        right = final_list[1]
        merged = [left[0] + right[0], left[1] + right[1], [left, right]]
        final_list.pop(0)
        final_list.pop(0)
        for i in range(len(final_list)):
            if final_list[i][0] > merged[0]:
                final_list.insert(i, merged)
                break
        else:
            final_list.append(merged)
    
    final_list = final_list[0]
    
    code_dict = {}
    generate_codes(final_list, '')

    bit_out = ""

    for byte in content:
        bit_out += code_dict[byte]
    
    make_file(bit_out, code_dict, output_path)