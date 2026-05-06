import numpy as np
import scipy.io.wavfile as wavfile
import encoder_lib
import os
import sys

os.makedirs("results", exist_ok=True)
os.makedirs("output", exist_ok=True)

input_file = "input/stego_standard.wav"
temp_file = "output/temp_invert.wav"

try:
    samplerate, data = wavfile.read(input_file)
except FileNotFoundError:
    print("[!] Loi: Khong tim thay file. Hay chay setup_attack.py truoc!")
    sys.exit(1)

print("[*] Bat dau kiem thu Tan cong Dao pha (Invert Attack)...")

# 1. Dao nguoc tin hieu (Nhan tat ca sample voi -1)
attacked_data = (data * -1).astype(np.int16)

# 2. Ghi ra file tam
wavfile.write(temp_file, samplerate, attacked_data)

# 3. Giai ma file tam
dec_result = encoder_lib.decode(temp_file, 6, seg_len=4096, start_bin=1500)

# 4. In ket qua
decoded_text = dec_result.get("decoded", "")
error_msg = dec_result.get("error")
is_survived = (decoded_text == "SECRET") and (error_msg is None)

print(f"[-] Dao pha (Invert) | Song sot: {is_survived} | Text: '{decoded_text}'")
