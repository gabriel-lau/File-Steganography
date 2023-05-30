# Function to convert an integer to binary string
def int_to_bin(n):
    return bin(n)[2:].zfill(8)

# Function to convert a binary string to integer
def bin_to_int(binary):
    return int(binary, 2)

def format_bin_msg(bin_msg, num_lsb):
    split_bin_msg = []
    for i in range(0, len(bin_msg), num_lsb):
        split_bin_msg.append(bin_msg[i:i + num_lsb])

    if len(split_bin_msg[-1]) % num_lsb != 0:
        split_bin_msg[-1] += '0' * (num_lsb - len(split_bin_msg[-1]) % num_lsb)

    return split_bin_msg

def find_mdat_box(file_path):
    with open(file_path, 'rb') as mp4_file:
        while True:
            box_size_bytes = mp4_file.read(4)
            if box_size_bytes == b'':
                # Reached the end of the file without finding 'mdat' box
                return None
            
            box_size = int.from_bytes(box_size_bytes, byteorder='big')
            box_type = mp4_file.read(4).decode('utf-8')
            
            if box_type == 'mdat':
                # Found 'mdat' box, return its position and size
                mdat_position = mp4_file.tell()

                # If mdat position is greater than box size, then the metadata might be corrupted
                # Another method of calculating mdat size will be used instead
                if mdat_position > box_size:
                    mp4_file.read()
                    box_size = mp4_file.tell() - mdat_position
                return mp4_file.tell(), box_size
            else:
                # Skip to the next box
                mp4_file.seek(box_size - 8, 1)