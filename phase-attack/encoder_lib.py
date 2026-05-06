import numpy as np
import scipy.io.wavfile as wavfile

def encode(input_wav, message, seg_len=4096, start_bin=1500):
    fs, data = wavfile.read(input_wav)
    orig_dtype = data.dtype
    
    if len(data.shape) > 1:
        data = data[:, 0]
    data = data.astype(np.float64)

    bits = np.unpackbits(np.frombuffer(message.encode('utf-8'), dtype=np.uint8))
    n_segs = int(np.floor(len(data) / seg_len))
    
    if n_segs == 0:
        return {"error": "Audio too short", "output": None, "fs": fs, "orig_dtype": orig_dtype}

    audio_segs = data[:n_segs * seg_len].reshape((n_segs, seg_len))
    freqs = np.fft.fft(audio_segs)
    mags = np.abs(freqs)
    phases = np.angle(freqs)

    # Năng lượng của "sóng mang" (Carrier wave) để bảo vệ góc pha
    # Mức 10.000.000 trong FFT (N=4096) tương đương biên độ ~4800 ở time-domain
    carrier_mag = 10000000.0

    for i, bit in enumerate(bits):
        if i >= (seg_len // 2 - start_bin): break
        
        # 1. Mã hóa bit vào góc Pha (Phase Coding)
        new_phase = np.pi/2 if bit == 1 else -np.pi/2
        phases[0, start_bin + i] = new_phase
        phases[0, seg_len - (start_bin + i)] = -new_phase
        
        # 2. Bơm năng lượng (Magnitude) để pha có chỗ bám, chống lại nhiễu
        mags[0, start_bin + i] = carrier_mag
        mags[0, seg_len - (start_bin + i)] = carrier_mag

    freqs_new = mags * np.exp(1j * phases)
    audio_segs_new = np.fft.ifft(freqs_new).real
    
    output_data = np.copy(data)
    output_data[:n_segs * seg_len] = audio_segs_new.flatten()

    return {"error": None, "output": output_data, "fs": fs, "orig_dtype": orig_dtype}

def decode(input_wav, num_chars, seg_len=4096, start_bin=1500):
    try:
        fs, data = wavfile.read(input_wav)
        if len(data.shape) > 1:
            data = data[:, 0]
        data = data.astype(np.float64)

        n_segs = int(np.floor(len(data) / seg_len))
        if n_segs == 0: return {"error": "Audio too short", "decoded": ""}

        audio_segs = data[:n_segs * seg_len].reshape((n_segs, seg_len))
        freqs = np.fft.fft(audio_segs)
        phases = np.angle(freqs)

        num_bits = num_chars * 8
        
        # Rút trích bit: Pha > 0 là bit 1, ngược lại là bit 0
        extracted_bits = [1 if phases[0, start_bin + i] > 0 else 0 for i in range(num_bits)]

        bits_arr = np.array(extracted_bits)
        chars = bits_arr.reshape((-1, 8)).dot(1 << np.arange(7, -1, -1)).astype(np.uint8)
        decoded = ''.join(chr(c) for c in chars if 32 <= c <= 126) 

        return {"error": None, "decoded": decoded}
    except Exception as e:
        return {"error": str(e), "decoded": ""}

def save_wav(audio_data, fs, filename, dtype):
    # Cắt xén an toàn (Clipping) để tránh lỗi tràn số khi ta bơm thêm năng lượng
    if dtype == np.int16:
        audio_data = np.clip(audio_data, -32768, 32767)
    wavfile.write(filename, fs, audio_data.astype(dtype))
