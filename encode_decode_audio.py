import wave
from av_steg_utils import int_to_bin, bin_to_int, format_bin_msg

def encode_audio(audio_path, payload, num_lsb):
    """encodes a audio file using lsb replacement

    Args:
        audio_path (string): path to audio file cover object
        payload (string): message to hide
        num_lsb (int): number of lsb to replace

    Raises:
        ValueError: if file format is not supported
    """
    if audio_path.endswith('.mp3'):
        return encode_mp3(audio_path, payload, num_lsb)
    elif audio_path.endswith('.wav'):
        return encode_wav(audio_path, payload, num_lsb)
    else:
        raise ValueError("Unsupported audio file format.")
    
def decode_audio(audio_path, num_lsb):
    """decodes a audio file encoded using lsb replacement

    Args:
        audio_path (string): path to audio file stego object
        num_lsb (int): number of replaced lsb

    Returns:
        string: payload

    Raises:
        ValueError: if file format is not supported
    """
    if audio_path.endswith('.mp3'):
        return decode_mp3(audio_path, num_lsb)
    elif audio_path.endswith('.wav'):
        return decode_wav(audio_path, num_lsb)
    else:
        raise ValueError("Unsupported audio file format.")

def encode_wav(audio_path, payload, num_lsb):
    payload = payload + 'EOM'
    # Open the audio file
    audio = wave.open(audio_path, mode='rb')
    frames = audio.readframes(audio.getnframes())
    samples = list(frames)

    # Convert the secret message to binary
    binary_message = ''.join(format(ord(c), '08b') for c in payload)

    formatted_bin_msg = format_bin_msg(binary_message, num_lsb)

    # Check if the secret message can fit in the audio file
    required_samples = len(formatted_bin_msg)
    max_samples = len(samples)

    if required_samples > max_samples:
        raise ValueError(f"Insufficient samples to hide the message.\nAudio samples: {max_samples}\nRequired samples: {required_samples}")
    
    # Modify the least significant bits of each sample to encode the message
    sample_index = 0

    for i in range(required_samples):
        sample = samples[sample_index]
        sample_bin = int_to_bin(sample)
        modified_sample_bin = sample_bin[:-num_lsb] + formatted_bin_msg[i]
        # modified_sample_bin =  formatted_bin_msg[i] + sample_bin[num_lsb:]
        modified_sample = bin_to_int(modified_sample_bin)
        samples[sample_index] = modified_sample

        sample_index += 1

    # Save the modified audio file with the hidden message
    modified_frames = bytes(samples)
    modified_audio = wave.open("encoded_audio.wav", mode='wb')
    modified_audio.setparams(audio.getparams())
    modified_audio.writeframes(modified_frames)
    modified_audio.close()
    audio.close()

    return "encoded_audio.wav" # required_samples

def decode_wav(audio_path, num_lsb):
    # Open the audio file
    audio = wave.open(audio_path, mode='rb')
    frames = audio.readframes(audio.getnframes())
    samples = list(frames)

    secret_message = ''
    chr_bin = ''

    for sample in samples:
        sample_bin = int_to_bin(sample)

        chr_bin += sample_bin[-num_lsb:]

        if len(chr_bin) >= 8:
            secret_message += chr(int(chr_bin[:8], 2))
            chr_bin = chr_bin[8:]

        if secret_message.endswith('EOM'):
            break
        # binary_message += sample_bin[:num_lsb]

    audio.close()

    return secret_message[:-3]

# Function to hide the secret message in the audio file
def encode_mp3(audio_path, payload, num_lsb):
    payload = payload + 'EOM'

    binary_payload = ''

    for e in payload:
        binary_payload += format(ord(e), '08b')

    binary_payload = format_bin_msg(binary_payload, num_lsb)

    file = open(audio_path, 'rb')
    data = bytearray(file.read())
    file.close()

    required_samples = len(binary_payload)
    max_samples = len(data)

    if required_samples > max_samples:
        raise ValueError(f"Insufficient samples to hide the message.\nAudio samples: {max_samples}\nRequired samples: {required_samples}")

    for i, b in enumerate(binary_payload):
        data[i] = (data[i] & (0xFF << num_lsb)) | int(b, 2)

    file = open('encoded_audio.mp3', 'wb')
    file.write(data)
    file.close()
    
    return 'encoded_audio.mp3'

# Function to extract the secret message from the audio file
def decode_mp3(audio_path, num_lsb):
    file = open(audio_path, 'rb')

    data = bytearray(file.read())
    file.close()

    payload = ''
    chr_bin = ''

    for d in data:
        chr_bin += int_to_bin(d)[-num_lsb:]

        if len(chr_bin) >= 8:
            payload += chr(int(chr_bin[:8], 2))
            chr_bin = chr_bin[8:]

        if payload.endswith('EOM'):
            break

    return payload[:-3]