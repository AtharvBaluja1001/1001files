import sys

def reconstruct_code_dict(header_content, txtfile:bool):
    code_dict = {}
    i = 0
    while i < len(header_content) - 3:  # ignore the trailing '\n\n\n'
        symbol = header_content[i:i+1]
        i += 1

        code_len = header_content[i]
        i += 1

        num_code_bytes = (code_len + 7) // 8
        code_bytes = header_content[i:i + num_code_bytes]
        i += num_code_bytes

        # Convert the code bytes to a binary string
        code_int = int.from_bytes(code_bytes, 'big')
        code_bin = bin(code_int)[2:].zfill(code_len)

        # Store in reverse (for decoding): code → symbol
        if txt:
            code_dict[code_bin] = symbol.decode("utf-8")
        else:
            code_dict[code_bin] = symbol

    return code_dict



if __name__ == "__main__":
    args = sys.argv
    file_path = args[1]
    file_type = file_path[file_path.find(".")+1:]
    output_path = args[2]

    if  "1001txt" in file_type:
        txt = True
    else:
        txt = False

    with open(file_path, "rb") as file:
        content = file.read()
    
    with open(file_path, "rb") as file:
        total_bits_bytes = file.read(4)
        total_bits = int.from_bytes(total_bits_bytes, byteorder="little")
    
        header_content = b''

        while not header_content.endswith(b'\n\n\n'):
            header_content += file.read(1)
        
        bit_bytes = file.read()
    
    bit_string = ''.join(f"{byte:08b}" for byte in bit_bytes)
    bit_string = bit_string[:total_bits]

    decoded_content = ""

    code_dict = reconstruct_code_dict(header_content, txt)

    t=""
    for bit in bit_string:
        t+=bit
        if t in code_dict:
            decoded_content+=code_dict[t]
            t=""
    
    with open(output_path, "w") as file:
        file.write(decoded_content)