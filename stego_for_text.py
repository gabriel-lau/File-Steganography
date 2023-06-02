"""
hello yes, erm you need to change the document paths under main if you wanna run this script separately.
this is before integration ^^ [for .txt files]
"""
import os


def encode_to_txt(cover_file, payload):
    with open(cover_file, 'r') as base:
        base_text = base.read()

    payload_bin = ''.join(format(ord(c), '08b') for c in payload)

    zero_char = '\u200B'  # zero-width space
    one_char = '\u200C'  # zero-width non-joiner
    boundary_char = '\u200D'  # zero-width joiner

    stego_text = boundary_char
    for bit in payload_bin:
        if bit == '0':
            stego_text += zero_char
        else:
            stego_text += one_char

    stego_text = base_text + stego_text

    root, ext = os.path.splitext(cover_file)
    dir_path = os.path.dirname(root)
    base_name = os.path.splitext(os.path.basename(cover_file))[0]
    output = base_name + "_encoded" + ext
    print('out_file_name:', output)
    print('directory_path', dir_path)
    stego_file = os.path.join(dir_path, output)

    with open(stego_file, 'w', encoding='utf-8') as stego:
        stego.write(stego_text)
    print("a very successful file creation has occurred :')")


def decode_frm_txt(stego_file):
    with open(stego_file, 'r', encoding='utf-8') as stego:
        stego_text = stego.read()

    find_start = stego_text.find('\u200D') + 1

    payload_chars = stego_text[find_start:]

    payload_bin = ''
    for char in payload_chars:
        if char == '\u200B':
            payload_bin += '0'
        elif char == '\u200C':
            payload_bin += '1'
        else:
            payload_bin += ' '

    decoded_text = ''
    for i in range(0, len(payload_bin), 8):
        byte = payload_bin[i:i + 8]
        decoded_text += chr(int(byte, 2))

    return decoded_text


if __name__ == '__main__':
    payload = "jed was here wajkakjakakkaa"
    cover_file = r"C:\Users\USER\PycharmProjects\stegosaurus\Text\base_text.txt"
    stego_file = r"C:\Users\USER\PycharmProjects\stegosaurus\Text\base_text_encoded.txt"
    encode_to_txt(cover_file, payload)
    decoded_text = decode_frm_txt(stego_file)
    print("decoded thingy:", decoded_text)