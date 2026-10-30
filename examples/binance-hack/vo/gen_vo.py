import pathlib
import numpy as np, soundfile as sf

base = pathlib.Path(__file__).parent
base.mkdir(exist_ok=True)

segments = [
    "Binance vừa bị hack. Đây là vụ trộm tiền ảo lớn nhất trong lịch sử.",
    "Kỷ lục cũ là vụ Bybit năm hai nghìn hai mươi lăm, mất một phẩy năm tỉ đô la.",
    "Lần này, Chainalysis ước tính số tiền bị lấy lên tới năm phẩy chín tỉ đô la, gấp bốn lần kỷ lục cũ.",
    "Ba tỉ đô la đã bị đóng băng. Bitcoin rơi năm phần trăm. Binance tạm dừng rút tiền, và tuyên bố sẽ bồi hoàn toàn bộ.",
]

from vieneu import Vieneu
tts = Vieneu()
for i, text in enumerate(segments):
    out = base / f"seg{i}.wav"
    audio = tts.infer(text, voice="Xuân Vĩnh")
    sf.write(str(out), audio, 48000)
    print(f"seg{i}: {len(audio)/48000:.2f}s :: {text}", flush=True)
print("VO_DONE", flush=True)
