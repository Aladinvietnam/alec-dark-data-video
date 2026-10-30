import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

base = Path(__file__).parent
import os
POLICY = os.environ.get("ALEC_WEBGL_POLICY", "webgl-policy.txt")
SHA = "c5c85869591ff8b3491450f49cfd62912c6dd41e5cecada4e831191d3185035e"
ARGS = ["--no-sandbox", "--allow-file-access-from-files", "--disable-gpu",
        f"--hatch-webgl-allowed-domains-file={POLICY}",
        f"--hatch-webgl-allowed-domains-sha256={SHA}"]

STILLS = [
    (0, 4.4, "border-flood"), (1, 5.0, "chat-thread"), (2, 4.8, "case-file"),
    (3, 3.4, "bar-race"), (4, 4.6, "money-river"), (5, 4.6, "rise-and-fall"),
    (6, 4.4, "paper-collage"), (7, 4.4, "threshold-tracker"), (8, 3.4, "slider-evidence"),
    (9, 3.6, "analog-horror"), (10, 4.4, "alert-hijack"), (11, 4.8, "ghost-radio"),
    (12, 4.4, "hundred-candles"),
]

mode = sys.argv[1] if len(sys.argv) > 1 else "stills"
(base / "stills_ns").mkdir(exist_ok=True)
(base / "frames_ns").mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH", "chromium"), args=ARGS)
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(f"file://{base}/newstyles.html")
    pg.wait_for_function("window.__ready === true")
    pg.evaluate("Promise.all([document.fonts.load('64px BVPBlack'), document.fonts.load('30px BVPXBold'), document.fonts.load('24px BVPSemi'), document.fonts.load('24px PlexMono')]).then(()=>{window.__fl=true})")
    pg.wait_for_function("window.__fl === true")
    pg.wait_for_timeout(500)
    if mode == "stills":
        for i, lt, name in STILLS:
            start = max(0.0, lt - 1.6)
            for w in range(49):
                pg.evaluate(f"window.renderScene({i}, {start + (lt - start) * w / 48})")
            pg.evaluate(f"window.renderScene({i}, {lt})")
            pg.wait_for_timeout(120)
            out = base / "stills_ns" / f"{name}.png"
            pg.screenshot(path=str(out))
            print("still", out, flush=True)
    else:
        frames = base / "frames_ns"
        total = 2145
        for i in range(total):
            fn = frames / f"f{i:04d}.jpg"
            if not fn.exists():
                pg.evaluate(f"window.render({i/30})")
                pg.screenshot(path=str(fn), type="jpeg", quality=82)
            if i % 200 == 0:
                print("frame", i, flush=True)
        print("CAPTURE_DONE", total, flush=True)
    b.close()
