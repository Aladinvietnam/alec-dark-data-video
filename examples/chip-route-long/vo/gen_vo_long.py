import pathlib
import soundfile as sf

base = pathlib.Path(__file__).parent
segments = [
    "Chín mươi phần trăm chip tiên tiến nhất thế giới được làm trên một hòn đảo. Và gần như mọi con chip đều phải đi qua một eo biển rộng chỉ một trăm ba mươi cây số.",
    "Đây là hành trình của một con chip AI. Nó ra đời tại Đài Loan, trong những nhà máy của TSMC, nơi làm ra hơn chín mươi phần trăm chip tiên tiến của toàn cầu.",
    "Nhưng Đài Loan không thể làm một mình. Cỗ máy in chip quan trọng nhất đến từ Hà Lan. Mỗi chiếc giá tới ba trăm tám mươi triệu đô la, và chỉ một công ty trên thế giới làm được.",
    "Từ những tấm wafer đó, chip lên đường tới thung lũng Silicon, và trở thành máy chủ AI trong các trung tâm dữ liệu lớn nhất hành tinh.",
    "Vấn đề nằm ở eo biển này. Theo viện nghiên cứu CSIS của Mỹ, hai nghìn bốn trăm năm mươi tỉ đô la hàng hoá đi qua đây mỗi năm, hơn một phần năm thương mại đường biển toàn cầu.",
    "Chuỗi cung ứng này mong manh vì ba lý do. Sản xuất dồn vào một hòn đảo. Máy móc chỉ có một nhà cung cấp duy nhất. Và mọi tuyến đường đều phải chung một eo biển.",
    "Thế giới đang chạy đua để thay đổi điều đó, với nhà máy mới mọc lên ở Mỹ, Nhật Bản và Đức. Nhưng ngay lúc này, cả kỷ nguyên AI vẫn đang đi qua một eo biển duy nhất.",
]

from vieneu import Vieneu
tts = Vieneu()
for i, text in enumerate(segments):
    audio = tts.infer(text, voice="Xuân Vĩnh")
    out = base / f"long{i}.wav"
    sf.write(str(out), audio, 48000)
    print(f"long{i}: {len(audio)/48000:.2f}s :: {text}", flush=True)
print("LONG_VO_DONE", flush=True)
