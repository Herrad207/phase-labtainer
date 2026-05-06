import numpy as np
import scipy.io.wavfile as wavfile
import encoder_lib
import csv
import os
import sys

os.makedirs("results", exist_ok=True)
os.makedirs("output", exist_ok=True)

input_file = "input/stego_standard.wav"
output_csv = "results/volume_attack.csv"
temp_file = "output/temp_volume.wav"

try:
    samplerate, data = wavfile.read(input_file)
except FileNotFoundError:
    print("[!] Loi: Khong tim thay file. Hay chay setup_attack.py truoc!")
    sys.exit(1)

scale_values = [0.2, 0.5, 1.5, 2.0]

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["scale", "decode_ok"])

    print("[*] Bat dau kiem thu Tan cong Am luong (Volume Attack)...")
    
    for scale in scale_values:
        # 1. Nhan bien do voi ty le scale va gioi han chong tran so (clipping)
        attacked_data = np.clip(data * scale, -32768, 32767).astype(np.int16)
        
        # 2. Ghi ra file tam
        wavfile.write(temp_file, samplerate, attacked_data)
        
        # 3. Giai ma
        dec_result = encoder_lib.decode(temp_file, 6, seg_len=4096, start_bin=1500)
        
        # 4. Kiem tra ket qua
        decoded_text = dec_result.get("decoded", "")
        error_msg = dec_result.get("error")
        is_survived = (decoded_text == "SECRET") and (error_msg is None)
        
        # 5. Ghi vao CSV cho Labtainer cham diem
        writer.writerow([scale, is_survived])
        
        # 6. In log hien thi
        print(f"Scale={scale:<4} | Song sot: {is_survived} | Text: '{decoded_text}'")

print("\n[*] Hoan thanh! Hay kiem tra file:", output_csv)
