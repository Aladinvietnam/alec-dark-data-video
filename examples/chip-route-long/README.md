# Ví dụ bản dài: The Chip Route

Video hoàn chỉnh 68 giây sản xuất theo skill này, định dạng **bản dài có hook, panel ảnh minh họa và lớp hiệu ứng âm thanh riêng**. Toàn bộ số liệu là số thật đã kiểm chứng, ghi trong [SOURCES.md](SOURCES.md).

## Cấu trúc 7 nhịp

| Nhịp | Thời gian | Nội dung | Hiệu ứng hình | Hiệu ứng tiếng |
|---|---|---|---|---|
| Hook | 0–9 giây | 90% chip tiên tiến làm trên một đảo, qua một eo biển 130 km | Target Lock lao vào eo biển, số đỏ đếm lên | Tick khi số đếm, bip khoá mục tiêu, impact |
| 1 | 9–19 giây | Đài Loan, nơi chip ra đời (TSMC) | Map Tour + panel ảnh phòng sạch | Whoosh camera, pop khi panel hạ |
| 2 | 19–29 giây | Hà Lan, máy EUV 380 triệu đô la của ASML | Cung vàng tự vẽ + panel ảnh máy EUV, số đếm | Pop, nhịp nhạc vào |
| 3 | 29–36 giây | Thung lũng Silicon, trung tâm dữ liệu AI | Cung thứ hai + panel ảnh data center | Whoosh |
| 4 | 36–47 giây | Eo biển gánh 2,45 nghìn tỉ đô la/năm (CSIS) | Khoá mục tiêu lần hai + panel ảnh tàu container | Tick, impact nhẹ |
| 5 | 47–56 giây | Ba điểm mong manh của chuỗi cung ứng | Bảng bằng chứng 3 hàng trượt vào | Pop theo từng hàng |
| 6 | 56–68 giây | Cuộc đua đa dạng hoá + bảng chốt 3 con số | 3 nhà máy mới phát sáng, bảng tổng kết | Riser + impact chốt |

## Cách chạy

Cần: Python 3, Playwright + Chromium, ffmpeg, phông Be Vietnam Pro (Black, ExtraBold, SemiBold) và VieNeu-TTS cho giọng đọc (giọng Xuân Vĩnh, tốc độ thường).

```sh
export ALEC_FONT_DIR=/duong/dan/thu/muc/font   # thư mục chứa 3 file .ttf ở trên
export CHROME_PATH=/duong/dan/chromium        # tuỳ chọn

python3 vo/gen_vo_long.py        # sinh 7 đoạn giọng vào vo_v2/ (chỉnh đường dẫn trong file nếu cần)
python3 gen_audio_long.py        # sinh music_long.wav và sfx_long.wav
python3 gen_long.py              # sinh long.html
python3 capture_long.py stills   # chụp thử các khung kiểm tra
python3 capture_long.py full     # chụp 2040 khung hình
# ghép bằng ffmpeg: 7 đoạn giọng đặt tại 0,4 / 9,2 / 19,0 / 28,8 / 36,4 / 46,9 / 56,2 giây,
# nhạc nền ở mức 0,26, lớp SFX ở mức 0,9, giới hạn đỉnh 0,89
```

Ảnh trong `imgs/` là ảnh minh họa sinh bằng AI; trên video mỗi panel đều có chú thích địa điểm và thẻ ILLUSTRATION.
