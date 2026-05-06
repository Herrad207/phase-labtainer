import numpy as np
import scipy.io.wavfile as wavfile
import encoder_lib
import csv
import os
import sys

os.makedirs("results", exist_ok=True)
os.makedirs("output", exist_ok=True)

input_file = "input/stego_standard.wav"
temp_file = "output/temp_noise.wav"
output_csv = "results/noise_attack.csv"

try:
    samplerate, data = wavfile.read(input_file)
except FileNotFoundError:
    print(f"[!] Loi: Khong tim thay file {input_file}")
    sys.exit(1)

# Khoi tao file CSV (Ghi de neu da ton tai) va tao dong Tieu de
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["sigma", "decode_ok"])

print("\n" + "=" * 55)
print("[*] CONG CU TAN CONG NHIEU LIEN TUC (PHASE CODING)")
print("[-] Nhap mot so de test muc do nhieu Sigma.")
print(f"[-] Ket qua se duoc tu dong luu vao: {output_csv}")
print("[-] Go 'q' hoac 'exit' de thoat chuong trinh.")
print("=" * 55 + "\n")

while True:
    user_input = input("[?] Nhap Sigma: ").strip()
    
    if user_input.lower() in ['q', 'quit', 'exit']:
        print(f"[*] Da thoat chuong trinh! Hay chay lenh 'checkwork'.\n")
        break
        
    if not user_input:
        continue

    try:
        sigma = float(user_input)
    except ValueError:
        print("    [!] Loi: Vui long nhap mot con so hop le!\n")
        continue

    # 1. Tao nhieu va cong vao du lieu goc
    noise = np.random.normal(0, sigma, data.shape)
    attacked_data = np.clip(data + noise, -32768, 32767).astype(np.int16)

    # 2. Ghi ra file tam va Giai ma
    wavfile.write(temp_file, samplerate, attacked_data)
    dec_result = encoder_lib.decode(temp_file, 6, seg_len=4096, start_bin=1500)

    # 3. Trich xuat thong tin
    decoded_text = dec_result.get("decoded", "")
    error_msg = dec_result.get("error")
    is_survived = (decoded_text == "SECRET") and (error_msg is None)

    # 4. GHI KET QUA VAO FILE CSV CHO HE THONG CHAM DIEM
    with open(output_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sigma, is_survived])

    # 5. In log ra man hinh
    if is_survived:
        print(f"    [+] [SONG SOT] Text: '{decoded_text}'")
    else:
        print(f"    [-] [GUC NGA]  Text: '{decoded_text}'")
        if error_msg:
            print(f"        Loi: {error_msg}")
    print("-" * 55)
