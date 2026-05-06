import numpy as np
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import encoder_lib
import os
import sys

os.makedirs("output", exist_ok=True)

input_file = "input/stego_standard.wav"
temp_file = "output/temp_resample.wav"

# ==========================================
# CHUAN BI DU LIEU (Chi doc 1 lan duy nhat)
# ==========================================
try:
    samplerate, data = wavfile.read(input_file)
except FileNotFoundError:
    print(f"[!] Loi: Khong tim thay file {input_file}. Hay chay setup truoc!")
    sys.exit(1)

print("\n" + "=" * 55)
print("[*] CONG CU TAN CONG RESAMPLE LIEN TUC")
print(f"[-] Tan so lay mau goc (Original Sample Rate): {samplerate} Hz")
print("[-] Nhap tan so lay mau moi de test (VD: 44099, 22050, 48000).")
print("[-] Go 'q' hoac 'exit' de thoat.")
print("=" * 55 + "\n")

# ==========================================
# VONG LAP NHAP VA TEST LIEN TUC
# ==========================================
while True:
    user_input = input(f"[?] Nhap Tan so moi (Goc dang la {samplerate}Hz): ").strip()
    
    if user_input.lower() in ['q', 'quit', 'exit']:
        print("[*] Da thoat chuong trinh test!\n")
        break
        
    if not user_input:
        continue

    try:
        new_sr = int(user_input)
        if new_sr <= 0:
            print("    [!] Loi: Tan so phai lon hon 0!\n")
            continue
    except ValueError:
        print("    [!] Loi: Vui long nhap mot so nguyen!\n")
        continue

    if new_sr == samplerate:
        print("    [-] Day la tan so goc, thuat toan chac chan song sot.\n")
        continue

    # 1. Tinh toan so luong sample moi dua tren ty le
    num_samples = int(len(data) * float(new_sr) / samplerate)
    
    # 2. Thuc hien resample mang du lieu
    attacked_data = signal.resample(data, num_samples).astype(np.int16)
    
    # 3. Ghi file voi tan so lay mau moi va Giai ma
    wavfile.write(temp_file, new_sr, attacked_data)
    dec_result = encoder_lib.decode(temp_file, 6, seg_len=4096, start_bin=1500)

    # 4. Trich xuat thong tin
    decoded_text = dec_result.get("decoded", "")
    error_msg = dec_result.get("error")
    is_survived = (decoded_text == "SECRET") and (error_msg is None)

    # 5. In log ket qua
    if is_survived:
        print(f"    [+] [SONG SOT] Text: '{decoded_text}'")
    else:
        print(f"    [-] [GUC NGA]  Text: '{decoded_text}'")
        if error_msg:
            print(f"        Loi: {error_msg}")
    print("-" * 55)
