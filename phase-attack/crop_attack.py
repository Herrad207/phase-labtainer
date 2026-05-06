import numpy as np
import scipy.io.wavfile as wavfile
import encoder_lib
import csv
import os
import sys

os.makedirs("results", exist_ok=True)
os.makedirs("output", exist_ok=True)

input_file = "input/stego_standard.wav"
output_csv = "results/crop_attack.csv"
temp_file = "output/temp_crop.wav"

try:
    samplerate, data = wavfile.read(input_file)
except FileNotFoundError:
    print("[!] Loi: Khong tim thay file. Hay chay setup_attack.py truoc!")
    sys.exit(1)

# Khoi tao file CSV (Ghi de neu da ton tai) va tao dong Tieu de
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["crop_samples", "decode_ok"])

print("\n" + "="*65)
print("[*] CONG CU TAN CONG CAT XEN LIEN TUC (CROP ATTACK)")
print("[-] Nhap so sample muon cat bo o dau file de test.")
print("[-] Thuat toan bi lech pha va sap do ra sao? Hay tu kiem chung!")
print(f"[-] Ket qua se duoc tu dong luu vao: {output_csv}")
print("[-] Go 'q' hoac 'exit' de thoat chuong trinh.")
print("="*65 + "\n")

while True:
    user_input = input("[?] Nhap so sample can cat (Crop): ").strip()
    
    if user_input.lower() in ['q', 'quit', 'exit']:
        print("\n[*] Da thoat chuong trinh! Hay chay lenh 'checkwork'.\n")
        break
        
    if not user_input:
        continue

    try:
        crop = int(user_input)
        if crop < 0:
            print("    [!] Loi: So sample phai lon hon hoac bang 0!\n")
            continue
    except ValueError:
        print("    [!] Loi: Vui long nhap mot so nguyen!\n")
        continue

    # 1. Cat bo 'crop' sample tu dau mang du lieu
    attacked_data = data[crop:]
    
    # 2. Ghi am thanh bi cat xen ra file tam
    wavfile.write(temp_file, samplerate, attacked_data)
    
    # 3. Giai ma file am thanh bi loi thoi gian
    dec_result = encoder_lib.decode(temp_file, 6, seg_len=4096, start_bin=1500)
    
    # 4. Kiem tra ket qua text
    decoded_text = dec_result.get("decoded", "")
    error_msg = dec_result.get("error")
    is_survived = (decoded_text == "SECRET") and (error_msg is None)
    
    # 5. GHI KET QUA VAO FILE CSV (Mo che do 'a' - append de ghi tiep)
    with open(output_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([crop, is_survived])
    
    # 6. In log ket qua
    if is_survived:
        print(f"    [+] [SONG SOT] Crop = {crop:<4} | Text: '{decoded_text}'")
    else:
        print(f"    [-] [GUC NGA]  Crop = {crop:<4} | Text: '{decoded_text}'")
        if error_msg:
            print(f"        Loi: {error_msg}")
    print("-" * 65)
