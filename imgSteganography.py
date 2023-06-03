# image_path = "C:\\Users\\Joshua Ong\\PycharmProjects\\CSC2005-Coursework-1\\imageTest.png"
import cv2
import numpy as np
from PIL import Image
from PIL import GifImagePlugin


import os

def to_bin(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type is not supported")


def encode_image(image_path, secretData, number_of_bits):
    image = cv2.imread(image_path)

    max_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode: ", max_bytes)
    secretData += "#####"
    if len(secretData) > max_bytes:
        raise ValueError("Insufficient bits")
    print("Encoding image")

    dataIndex = 0
    binSecretData = to_bin(secretData)
    dataLen = len(binSecretData)
    counter = 128
    count = 0
    encode_text = open('encode.txt', 'w')
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            info = ""
            for i in range(number_of_bits):
                if dataIndex < dataLen:
                    info += binSecretData[dataIndex]
                    dataIndex += 1
                else:
                    info += "0"

            pixel[0] = int(r[:-number_of_bits] + info, 2)

            info = ""
            for i in range(number_of_bits):
                if dataIndex < dataLen:
                    info += binSecretData[dataIndex]
                    dataIndex += 1
                else:
                    info += "0"
            pixel[1] = int(g[:-number_of_bits] + info, 2)

            info = ""
            for i in range(number_of_bits):
                if dataIndex < dataLen:
                    info += binSecretData[dataIndex]
                    dataIndex += 1
                else:
                    info += "0"
            pixel[2] = int(b[:-number_of_bits] + info, 2)
            if count<counter:
                encode_text.write(str(pixel))
                encode_text.write('\n')
                count+=1

            if dataIndex >= dataLen:
                break
    encode_text.close()

    file_name, file_extension = os.path.splitext(image_path)

    cv2.imwrite(file_name + "_encoded" + file_extension, image,  [cv2.IMWRITE_JPEG_QUALITY, 100])
    print("Image successfully encoded: "+ file_name + "_encoded" + file_extension)

    return file_name + "_encoded" + file_extension


def decode_image(image_path, number_of_bits):
    print("Decoding image")
    image = cv2.imread(image_path)
    binData = ""

    counter = 128
    count = 0
    decode_text = open('decode.txt', 'w')

    for row in image:
        for pixel in row:
            if count < counter:
                decode_text.write(str(pixel))
                decode_text.write('\n')
                count += 1
            r, g, b = to_bin(pixel)
            binData += r[-number_of_bits:]
            binData += g[-number_of_bits:]
            binData += b[-number_of_bits:]
    decode_text.close()
    allBytes = [binData[i: i + 8] for i in range(0, len(binData), 8)]
    decodedData = ""
    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        if decodedData[-5:] == "#####":
            break
    print("Image successfully decoded")
    return decodedData[:-5]


# Example usage
# image_encode_path = "C:\\Users\\Joshua Ong\\PycharmProjects\\CSC2005-Coursework-1\\imageTest.png"
# image_decode_path = "C:\\Users\\Joshua Ong\\PycharmProjects\\CSC2005-Coursework-1\\imageTest_encoded.png"
# data_to_encode = "test secret"
# number_of_bits = 1
# Encode the data into the image
# encode_image(image_encode_path, data_to_encode, number_of_bits)

# Decode the data from the encoded image
# decoded_data = decode_image(image_decode_path, number_of_bits)
# print("Decoded data:", decoded_data)


# imageObject = Image.open("./testgif.gif")
# print("number of frames:", imageObject.n_frames)

# for frameIndex in range(0, imageObject.n_frames):
# imageObject.seek(0)
# frame = imageObject.copy()
# rgb_data = list(imageObject.convert('RGB').getdata())
# # r, g, b = rgb_data
# binary_data = []
# for rgb in rgb_data:
#     r,g,b = rgb
#     print(r)
