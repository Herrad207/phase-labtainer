import os

os.makedirs("results", exist_ok=True)
output_file = "results/answers.txt"

print("="*65)
print(" KIEM TRA KIEN THUC TONG HOP - PHASE CODING ATTACKS")
print("="*65)
print("Hay tra loi cac cau hoi sau dua tren ket qua thuc hanh cua ban.\n")

answers = {}

# CW2: Nguong Sigma
while True:
    try:
        ans_sigma = int(input("[Cau 1] Nguong nhieu Sigma toi da de ma bi mat con song sot la khoang bao nhieu? (Nhap 1 so nguyen): "))
        answers['CW2_SIGMA'] = ans_sigma
        break
    except ValueError:
        print("  -> Vui long nhap mot con so!")

print("\n(Cac cau hoi Yes/No hoac True/False: Nhap Y/N hoac T/F)")

# CW3: Resample
ans_resample = input("[Cau 2] Tan cong thay doi tan so lay mau (Resample) co pha huy duoc Phase Coding khong? (Yes/No): ").strip().lower()
answers['CW3_RESAMPLE'] = "yes" if ans_resample in ['y', 'yes', 't', 'true'] else "no"

# CW4: Volume
ans_volume = input("[Cau 3] Tan cong thay doi am luong (Volume) co pha huy duoc Phase Coding khong? (Yes/No): ").strip().lower()
answers['CW4_VOLUME'] = "yes" if ans_volume in ['y', 'yes', 't', 'true'] else "no"

# CW6: Invert Attack
print("\n[Cau 4] Hien tuong gi xay ra voi cac bit du lieu khi dao pha am thanh (Invert)?")
print("  A. Giu nguyen khong doi")
print("  B. Lat bit (Bit 0 thanh 1 va nguoc lai)")
print("  C. Bi xoa trang hoan toan")
ans_invert = input("Chon dap an (A/B/C): ").strip().upper()
answers['CW6_INVERT'] = ans_invert

# CW7/8: Crop Attack (Thay the cho viec bat do file CSV)
print("\n[Cau 5] Don tan cong nao la chi mang nhat do lam truot khung thoi gian (Time-shift) cua ham FFT?")
print("  A. Noise Attack")
print("  B. Volume Attack")
print("  C. Crop Attack")
ans_dangerous = input("Chon dap an (A/B/C): ").strip().upper()
answers['CW7_CROP_DANGEROUS'] = ans_dangerous

# Ghi ra file
with open(output_file, "w") as f:
    for key, value in answers.items():
        f.write(f"{key}:{value}\n")

print("\n" + "="*65)
print("[*] Da luu cau tra loi vao results/answers.txt")
print("[*] Hay chay lenh 'checkwork' de xem diem cua ban!")
print("="*65)
