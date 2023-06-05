from PIL import Image,ImageSequence, GifImagePlugin
import os


def to_bin(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, bytearray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type is not supported")


def encode_image(image_path, secret_data, number_of_bits):
    gif = Image.open(image_path)

    frames = []
    for frame in ImageSequence.Iterator(gif):
        image = frame.convert("RGB")
        frames.append(image.copy())

    max_bytes = frames[0].size[0] * frames[0].size[1] * 3 // 8
    print("Maximum bytes to encode: ", max_bytes)
    secret_data += "#####"
    if len(secret_data) > max_bytes:
        raise ValueError("Insufficient bits")
    print("Encoding image")

    data_index = 0
    bin_secret_data = to_bin(secret_data)
    data_len = len(bin_secret_data)
    counter = 128
    count = 0
    encode_text = open('encode.txt', 'w')
    for frame in frames:
        pixels = frame.load()
        for y in range(frame.size[1]):
            for x in range(frame.size[0]):
                r, g, b = pixels[x, y]
                r, g, b = to_bin(r), to_bin(g), to_bin(b)

                info = ""
                for i in range(number_of_bits):
                    if data_index < data_len:
                        info += bin_secret_data[data_index]
                        data_index += 1
                    else:
                        info += "0"
                
                r = int(r[:-number_of_bits] + info, 2)

                info = ""
                for i in range(number_of_bits):
                    if data_index < data_len:
                        info += bin_secret_data[data_index]
                        data_index += 1
                    else:
                        info += "0"
                
                g = int(g[:-number_of_bits] + info, 2)

                info = ""
                for i in range(number_of_bits):
                    if data_index < data_len:
                        info += bin_secret_data[data_index]
                        data_index += 1
                    else:
                        info += "0"
                
                b = int(b[:-number_of_bits] + info, 2)

                pixels[x, y] = (r, g, b)

                if count < counter:
                    encode_text.write(str((r, g, b)))
                    encode_text.write('\n')
                    count += 1

                if data_index >= data_len:
                    break

            if data_index >= data_len:
                break

        if data_index >= data_len:
            break

    encode_text.close()

    file_name, file_extension = os.path.splitext(image_path)
    #output_path = file_name + "_encoded" + file_extension
    output_path = "encoded_gif.gif"
    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, duration=gif.info['duration'])
    print(len(frames))

    print("Image successfully encoded: " + output_path)

    return output_path


def decode_image(image_path, number_of_bits):
    print("Decoding image")
    image = Image.open(image_path)
    frames = []
    for frame in ImageSequence.Iterator(image):
        frames.append(frame.convert("RGBA"))

    bin_data = ""
    counter = 128
    count = 0
    decode_text = open('decode.txt', 'w')

    for frame in frames:
        pixels = frame.load()
        for y in range(frame.size[1]):
            for x in range(frame.size[0]):
                if count < counter:
                    decode_text.write(str(pixels[x, y]))
                    decode_text.write('\n')
                    count += 1

                r, g, b, a = pixels[x, y]
                r, g, b = to_bin(r), to_bin(g), to_bin(b)

                bin_data += r[-number_of_bits:]
                bin_data += g[-number_of_bits:]
                bin_data += b[-number_of_bits:]

    decode_text.close()

    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":
            break

    print("Image successfully decoded")

    return decoded_data[:-5]
"""
# Example usage
image_path = 'bears.gif'
output_path = 'bears_encoded.gif'
message = "This is a secret message!"
number_of_bits = 1

# Hide the message in the GIF image
encode_image(image_path, message, number_of_bits)

# Reveal the message from the encoded GIF image
revealed_message = decode_image(output_path, number_of_bits)
print("Revealed message:", revealed_message)
"""