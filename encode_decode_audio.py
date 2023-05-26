import wave
from pydub import AudioSegment

def encode_audio(audio_path, payload, num_lsb):
    if audio_path.endswith('.mp3'):
        encode_mp3(audio_path, payload, num_lsb)
    elif audio_path.endswith('.wav'):
        encode_wav(audio_path, payload, num_lsb)
    else:
        raise ValueError("Unsupported audio file format.")
    
def decode_audio(audio_path, num_lsb):
    if audio_path.endswith('.mp3'):
        return decode_mp3(audio_path, num_lsb)
    elif audio_path.endswith('.wav'):
        return decode_wav(audio_path, num_lsb)
    else:
        raise ValueError("Unsupported audio file format.")

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

def mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

def wav_to_mp3(wav_file, mp3_file):
    audio = AudioSegment.from_wav(wav_file)
    audio.export(mp3_file, format="mp3")

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

    return required_samples

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


if __name__ == "__main__":
    # Example usage
    audio_path = 'ahh-snoring.mp3'
    secret_message = """According to all known laws of aviation, there is no way a bee should be able to fly. """
    num_lsb = 3

    encode_audio(audio_path, secret_message, num_lsb)

    extracted_message = decode_audio("encoded_audio.mp3", num_lsb)

    print("Extracted message:", extracted_message)