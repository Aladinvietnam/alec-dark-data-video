# Ví dụ: Binance Hacked — Chart Duel + Investigation

Mã nguồn của video thử nghiệm đầu tiên theo skill này: vụ hack Binance ngày 29/10/2026, ước tính 5,9 tỉ USD bị lấy (Chainalysis), gấp 4 lần kỷ lục Bybit 2025. Bản cuối dài 35,4 giây, 1920x1080, 30 fps, gồm 4 pha: cảnh báo mở đầu, cột Bybit, cột Binance với huy hiệu 4X, bảng điều tra nguyên nhân, và phần chốt đóng băng 3,0 tỉ USD.

Mọi con số và nguồn kiểm chứng nằm trong [SOURCES.md](SOURCES.md).

## Yêu cầu

- Python 3.11+ với `playwright` (và Chromium của Playwright, hoặc đặt biến `CHROME_PATH` trỏ tới bản Chromium có sẵn)
- `ffmpeg`
- Font Be Vietnam Pro (Black, ExtraBold, SemiBold) đặt trong thư mục `fonts/` cạnh `build_scene.py`, hoặc đặt biến `ALEC_FONT_DIR` trỏ tới thư mục chứa font
- (Tuỳ chọn, cho giọng đọc) VieNeu-TTS với giọng “Xuân Vĩnh”, xem `vo/gen_vo.py` và `vo/gen_vo_cause.py`

## Các bước

```bash
# 1. Sinh file cảnh HTML (font được nhúng dạng base64)
python build_scene.py

# 2. Soi khung hình tĩnh ở các mốc quan trọng trước khi render
python capture.py stills

# 3. Chụp toàn bộ 1062 khung hình
python capture.py full

# 4. Sinh nhạc nền (tổng hợp bằng numpy, 35,4 giây)
python gen_music.py

# 5. Sinh giọng đọc từng đoạn rồi chuẩn hoá âm lượng
python vo/gen_vo.py
python vo/gen_vo_cause.py

# 6. Ghép hình và tiếng bằng ffmpeg (5 đoạn giọng đặt theo mốc thời gian của từng pha)
ffmpeg -framerate 30 -i frames/f%04d.jpg -i <các file giọng> -i music.wav ...
```

Mốc đặt giọng trong bản gốc: đoạn mở đầu 0,35 giây; kỷ lục cũ 4,6 giây; con số chính 9,1 giây; đoạn điều tra 15,9 giây; đoạn chốt 27,2 giây. Nhạc giữ ở mức 0.30 âm lượng dưới giọng, toàn mix qua limiter 0.89.

## Lưu ý trung thực số liệu

Số 5,9 tỉ USD là **ước tính của Chainalysis** (Arkham đếm theo ví là 5,7 tỉ), video ghi rõ nhãn này trên màn hình. Ba phát hiện trong bảng điều tra đều là **nghi vấn chưa xác nhận** tại thời điểm sản xuất và được trình bày dạng câu hỏi kèm nguồn (Blockaid, Arkham qua CoinDesk).
