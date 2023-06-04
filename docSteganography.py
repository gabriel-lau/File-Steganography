# DOCCUMENT STEGANOGRAPHY
from lsb_txt import encode_to_txt, decode_from_txt
from lsb_docx import encode_to_doc, decode_frm_doc
from lsb_xlsx import hide_data_in_excel, extract_data_from_excel

def encode_doc(fileName, text, bits):
    if fileName.endswith(('.txt')):
        return encode_to_txt(fileName, text, bits)
    elif fileName.endswith(('.docx')):
        return encode_to_doc(fileName, text, bits)
    elif fileName.endswith(('.xlsx')):
        return hide_data_in_excel(fileName, text, bits)
    
def decode_doc(fileName, bits):
    if fileName.endswith(('.txt')):
        return decode_from_txt(fileName, bits)
    elif fileName.endswith(('.docx')):
        return decode_frm_doc(fileName, bits)
    elif fileName.endswith(('.xlsx')):
        return extract_data_from_excel(fileName, bits)