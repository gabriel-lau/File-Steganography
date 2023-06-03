# INTERFACE BETWEEN GUI AND THE STEGANOGRAPHY MODULES
import imgSteganography as img
import stego_for_doc as doc
import avSteganography as av

def encode(text, bits, fileName): # encode(text, bit, fileName) -> fileName
    if fileName.endswith(('.mp3', '.mp4', '.wav')):
        return av.encode_av(fileName, text, bits)
    if fileName.endswith(('.png', '.jpg')):
        return img.encode_image(fileName, text, bits)
    if fileName.endswith(('.docx')):
        return doc.encode_to_doc(fileName, text)
    return fileName

def decode(bits, fileName): # decode(bit, fileName) -> text
    if fileName.endswith(('.mp3', '.mp4', '.wav')):
        return av.decode_av(fileName, bits)
    if fileName.endswith(('.png', '.jpg')):
        return img.decode_image(fileName, bits)
    if fileName.endswith(('.docx')):
        return doc.decode_frm_doc(fileName)
    return fileName