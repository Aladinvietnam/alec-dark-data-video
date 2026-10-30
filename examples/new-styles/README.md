# Ví dụ: 13 phong cách thể loại mới (New Genre Styles)

Mã nguồn sản xuất reel giới thiệu 13 phong cách mở rộng của skill, nghiên cứu ngày 30/10/2026 từ các định dạng đang thịnh hành trên mạng xã hội (kể truyện, kinh tế, tin tức, truyện ma) và ghi vào SKILL.md dưới mục “Genre templates beyond the data set”. Ghi chú nghiên cứu đầy đủ nằm tại [references/genre-styles-research.md](../../references/genre-styles-research.md).

13 phong cách: Border Flood, Chat Thread, Case File, Bar Race, Money River, Rise and Fall, Paper Collage, Threshold Tracker, Slider Evidence, Analog Horror, Alert Hijack, Ghost Radio và Hundred Candles (phong cách phối gốc của skill: nghi lễ trăm nến kaidan kết hợp bộ đếm dữ liệu).

## Chạy

Cần: Python + Playwright + Chromium, bộ font Be Vietnam Pro và IBM Plex Mono Bold, file GeoJSON các quốc gia (`countries.geojson`, lấy từ johan/world.geo.json).

```bash
export ALEC_FONT_DIR=/duong/dan/font        # thư mục chứa BeVietnamPro-*.ttf và IBMPlexMono-Bold.ttf
export ALEC_GEOJSON=/duong/dan/countries.geojson
export CHROME_PATH=/duong/dan/chrome        # bỏ qua nếu Chromium mặc định của Playwright chạy được WebGL
export ALEC_WEBGL_POLICY=/duong/dan/webgl-policy.txt  # chỉ khi Chromium yêu cầu chính sách WebGL

python gen_newstyles.py        # sinh newstyles_part1.html (cảnh 1-6)
python gen_part2.py            # gắn cảnh 7-13 và bộ khung reel, cho ra newstyles.html
python capture_newstyles.py stills   # chụp 13 ảnh tĩnh vào stills_ns/
python gen_audio_newstyles.py        # sinh nhạc nền và SFX cho reel
python capture_newstyles.py full     # chụp 2145 khung hình của reel 71,5 giây
ffmpeg -framerate 30 -i frames_ns/f%04d.jpg -i bed_ns.wav -i sfx_ns.wav \
  -filter_complex "[1:a]volume=0.30[a1];[2:a]volume=0.9[a2];[a1][a2]amix=inputs=2:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -shortest new_styles_reel.mp4
```

Toàn bộ số liệu trong các cảnh đều là số mẫu để minh họa phong cách.
