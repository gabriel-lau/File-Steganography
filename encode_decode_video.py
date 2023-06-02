from av_steg_utils import find_mdat_box, int_to_bin, format_bin_msg

def encode_video(video_path, payload, num_lsb):
    """encodes a video file using lsb replacement

    Args:
        video_path (string): path to video file cover object
        payload (string): message to hide
        num_lsb (int): number of lsb to replace

    Raises:
        ValueError: if file format is not supported
    """
    if video_path.endswith('.mp4'):
        return encode_mp4(video_path, payload, num_lsb)
    else:
        raise ValueError('File format not supported.')
    
def decode_video(video_path, num_lsb):
    """decodes a video file encoded using lsb replacement

    Args:
        video_path (string): path to video file stego object
        num_lsb (int): number of replaced lsb

    Raises:
        ValueError: if file format is not supported
    """
    if video_path.endswith('.mp4'):
        return decode_mp4(video_path, num_lsb)
    else:
        raise ValueError('File format not supported.')

def encode_mp4(mp4_path, payload, num_lsb):
    mdat_position, mdat_size = find_mdat_box(mp4_path)

    file = open(mp4_path, 'rb')
    data = bytearray(file.read())
    file.close()

    payload = payload + 'EOM'

    binary_payload = ''
    
    for e in payload:
        binary_payload += format(ord(e), '08b')

    binary_payload = format_bin_msg(binary_payload, num_lsb)

    required_samples = len(binary_payload)

    if required_samples > mdat_size:
        raise ValueError(f"Insufficient samples to hide the message.\nAudio samples: {mdat_size}\nRequired samples: {required_samples}")
    
    for i in range(mdat_position, mdat_position + required_samples):
        # replace the last num_lsb bits of the byte with the payload
        data[i] = (data[i] & (0xFF << num_lsb)) | int(binary_payload[i - mdat_position], 2)

    file = open('encoded_video.mp4', 'wb')
    file.write(data)
    file.close()
    
    return 'encoded_video.mp4'

def decode_mp4(mp4_path, num_lsb):
    mdat_position = find_mdat_box(mp4_path)[0]

    file = open(mp4_path, 'rb')
    data = bytearray(file.read())
    file.close()


    payload = ''
    chr_bin = ''

    for i in range(mdat_position, len(data)):
        # get the last num_lsb bits of the byte
        chr_bin += int_to_bin(data[i])[-num_lsb:]

        # convert the binary string to a character when there are at least 8 bits
        if len(chr_bin) >= 8:
            payload += chr(int(chr_bin[:8], 2))
            chr_bin = chr_bin[8:]

        if payload.endswith('EOM'):
            break

    return payload[:-3]


