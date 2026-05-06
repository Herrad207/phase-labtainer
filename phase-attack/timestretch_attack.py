import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import encoder_lib
import csv
import os
import sys

os.makedirs("results", exist_ok=True)
os.makedirs("output", exist_ok=True)

input_file = "input/stego_standard.wav"
output_csv = "results/timestretch.csv"
temp_file = "output/temp_stretch.wav"

try:
    samplerate, data = wavfile.read(input_file)
except FileNotFoundError:
    print("[!] Loi: Khong tim thay file. Hay chay setup_attack.py truoc!")
    sys.exit(1)

stretch_factors = [0.8, 1.2, 1.5]

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["factor", "decode_ok"])

    print("[*] Bat dau kiem thu Tan cong Time Stretch...")
    
    for factor in stretch_factors:
        # 1. Tinh so luong mang moi
        new_len = int(len(data) * factor)
        
        # 2. Resample de keo gian hoac rut ngan thoi gian thuc te cua song am
        attacked_data = signal.resample(data, new_len).astype(np.int16)
        
        # 3. Ghi file voiw samplerate GOC (tao ra hieu ung chay nhanh/cham)
        wavfile.write(temp_file, samplerate, attacked_data)
        
        # 4. Giai ma
        dec_result = encoder_lib.decode(temp_file, 6, seg_len=4096, start_bin=1500)
        
        # 5. Kiem tra va luu ket qua
        decoded_text = dec_result.get("decoded", "")
        error_msg = dec_result.get("error")
        is_survived = (decoded_text == "SECRET") and (error_msg is None)
        
        writer.writerow([factor, is_survived])
        print(f"Factor={factor:<4} | Song sot: {is_survived} | Text: '{decoded_text}'")

print("\n[*] Hoan thanh! Hay kiem tra file:", output_csv)
