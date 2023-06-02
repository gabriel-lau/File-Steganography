from encode_decode_audio import encode_audio, decode_audio
from encode_decode_video import encode_video, decode_video

def encode_av(file_path, payload, num_lsb):
    """encodes an av file using lsb replacement

    Args:
        file_path (string): path to av file cover object
        payload (string): message to hide
        num_lsb (int): number of lsb to replace

    Raises:
        ValueError: if file format is not supported
    """
    if file_path.endswith(('.mp3', '.wav')):
        return encode_audio(file_path, payload, num_lsb)
    elif file_path.endswith('.mp4'):
        return encode_video(file_path, payload, num_lsb)
    else:
        raise ValueError('File format not supported.')
    
def decode_av(file_path, num_lsb):
    """decodes a av file encoded using lsb replacement

    Args:
        file_path (string): path to av file stego object
        num_lsb (int): number of replaced lsb

    Returns:
        string: payload

    Raises:
        ValueError: if file format is not supported
    """
    if file_path.endswith(('.mp3', '.wav')):
        return decode_audio(file_path, num_lsb)
    elif file_path.endswith('.mp4'):
        return decode_video(file_path, num_lsb)
    else:
        raise ValueError('File format not supported.')