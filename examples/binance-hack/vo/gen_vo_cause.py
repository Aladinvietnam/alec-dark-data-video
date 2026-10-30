import pathlib
import soundfile as sf

base = pathlib.Path(__file__).parent
text = ("Điều tra ban đầu cho thấy kẻ tấn công bị nghi đã can thiệp vào quá trình ký giao dịch, "
        "thay vì đánh cắp khóa bí mật. Sau đó, tiền bị đẩy qua các sàn phi tập trung, "
        "đổi sang những tài sản khó bị đóng băng hơn.")

from vieneu import Vieneu
tts = Vieneu()
audio = tts.infer(text, voice="Xuân Vĩnh")
out = base / "seg_cause.wav"
sf.write(str(out), audio, 48000)
print(f"seg_cause: {len(audio)/48000:.2f}s :: {text}", flush=True)
print("CAUSE_VO_DONE", flush=True)
