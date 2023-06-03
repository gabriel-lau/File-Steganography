"""
[for .txt files with LSB choice though idk why 0, 1 and 2 also dont work 0-0]
"""
import os


def encode_to_txt(base_file, payload, num_lsb):
    with open(base_file, 'r', encoding='utf-8') as file:
        base_text = file.read()

    payload_bin = ''.join(format(ord(c), '08b') for c in payload)

    zero_char = '\u200B'  # zero-width space
    one_char = '\u200C'  # zero-width non-joiner
    boundary_char = '\u200D'  # zero-width joiner

    stego_text = boundary_char

    for i in range(len(payload_bin)):
        bit = payload_bin[i]
        if i % 3 < num_lsb:
            if bit == '0':
                stego_text += zero_char
            else:
                stego_text += one_char
        else:
            stego_text += bit

    stego_text = base_text + stego_text

    root, ext = os.path.splitext(base_file)
    dir_path = os.path.dirname(root)
    base_name = os.path.splitext(os.path.basename(base_file))[0]
    output = base_name + f"_encoded" + ext
    encoded_file = os.path.join(dir_path, output)
    with open(encoded_file, 'w', encoding='utf-8') as file:
        file.write(stego_text)
    print('written to:', encoded_file)


def decode_from_txt(stego_file, num_lsb):
    with open(stego_file, 'r', encoding='utf-8') as file:
        stego_text = file.read()

    find_start = stego_text.find('\u200D') + 1

    payload = stego_text[find_start:]

    payload_bin = ''
    for i in range(len(payload)):
        char = payload[i]
        if i % 3 < num_lsb:
            if char == '\u200B':
                payload_bin += '0'
            elif char == '\u200C':
                payload_bin += '1'

    decoded_text = ''
    for i in range(0, len(payload_bin), 8):
        byte = payload_bin[i:i + 8]
        if len(byte) == 8:
            try:
                decoded_text += chr(int(byte, 2))
            except ValueError:
                break

    return decoded_text


if __name__ == '__main__':
    payload = "jed really doesnt know why half works and half dont"
    base_file = r"C:\Users\USER\PycharmProjects\stegosaurus\Text\base_text.txt"
    stego_file = r"C:\Users\USER\PycharmProjects\stegosaurus\Text\base_text_encoded.txt"

    num_lsb_to_use = 4  # (e.g., 0, 1, 2, ..., 5)
    encode_to_txt(base_file, payload, num_lsb_to_use)
    decoded_text = decode_from_txt(stego_file, num_lsb_to_use)
    print("decoded thingy:", decoded_text)
