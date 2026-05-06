#!/usr/bin/env python3
import numpy as np
import scipy.io.wavfile as wavfile
import sys
import os

sys.path.insert(0, '.')
from encoder_lib import encode, save_wav, decode

# 1. Đảm bảo thư mục input tồn tại
os.makedirs("input", exist_ok=True)

sr = 44100
t = np.arange(sr * 2) / sr

# 2. Xử lý thông minh cho Labtainers và Test Local
try:
    # Khi chạy trong Labtainers, hệ thống sẽ chèn số thật vào đây
    atk_amp1 = PARAM_AMP_1
    atk_amp2 = PARAM_AMP_2
except NameError:
    # Khi bạn chạy test thủ công ở ngoài, nó sẽ rớt xuống đây dùng giá trị mặc định
    atk_amp1 = 10000
    atk_amp2 = 5000

# 3. Tạo âm thanh
# (Sự xuất hiện của nhiễu trắng 500 * np.random... là CỰC KỲ QUAN TRỌNG. 
# Nó cung cấp năng lượng nền cho mọi tần số, giúp Phase Coding ở Bin 1500 có chỗ bám)
music = (atk_amp1 * np.sin(2 * np.pi * 440 * t) +
         atk_amp2 * np.sin(2 * np.pi * 880 * t) +
         500 * np.random.randn(len(t)))

# 4. Giới hạn biên độ an toàn trước khi ép kiểu để tránh tiếng click/rít do tràn số int16
audio = np.clip(music, -32768, 32767).astype(np.int16)
wavfile.write("input/audio_original.wav", sr, audio)

# 5. Nhúng mã bí mật
res = encode("input/audio_original.wav", "SECRET", seg_len=4096, start_bin=1500)
if res["error"] is None:
    save_wav(res["output"], res["fs"], "input/stego_standard.wav", res["orig_dtype"])
    print("[+] Khởi tạo thành công: input/stego_standard.wav")
else:
    print(f"[-] Lỗi mã hóa: {res['error']}")

# 6. Kiểm tra lại bằng hàm decode (Self-test)
dec = decode("input/stego_standard.wav", 6, seg_len=4096, start_bin=1500)
if dec["error"] is None:
    is_match = (dec['decoded'] == 'SECRET')
    # Ghi file verify.txt cho Labtainers chấm điểm hoặc kiểm tra
    with open("input/verify.txt", "w") as f:
        f.write(f"decoded:{dec['decoded']}\nmatch:{is_match}\n")
    
    print(f"[+] Kiểm định file: Giải mã ra '{dec['decoded']}' - Khớp: {is_match}")
else:
    print(f"[-] Lỗi giải mã lúc kiểm định: {dec['error']}")
