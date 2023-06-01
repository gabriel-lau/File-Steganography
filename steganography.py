# INTERFACE BETWEEN GUI AND THE STEGANOGRAPHY MODULES
import imgSteganography as img
import docSteganography as doc
import avSteganography as av

def encode(text, bits, fileName): # encode(text, bit, fileName) -> fileName
    if fileName.endswith(('.mp3', '.mp4', '.wav')):
        return av.encode(fileName, bits, text)
    return fileName

def decode(bits, fileName): # decode(bit, fileName) -> text
    
    return fileName