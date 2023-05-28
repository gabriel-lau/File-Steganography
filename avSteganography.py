from encode_decode_audio import encode_audio, decode_audio
from encode_decode_video import encode_video, decode_video

def encode_av(file_path, payload, num_lsb):
    if file_path.endswith(('.mp3', '.wav')):
        encode_audio(file_path, payload, num_lsb)
    elif file_path.endswith('.mp4'):
        encode_video(file_path, payload, num_lsb)
    else:
        raise ValueError('File format not supported.')
    
def decode_av(file_path, num_lsb):
    if file_path.endswith(('.mp3', '.wav')):
        return decode_audio(file_path, num_lsb)
    elif file_path.endswith('.mp4'):
        return decode_video(file_path, num_lsb)
    else:
        raise ValueError('File format not supported.')