import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

base = Path(__file__).parent
import os
POLICY = os.environ.get("ALEC_WEBGL_POLICY", "")
SHA = "c5c85869591ff8b3491450f49cfd62912c6dd41e5cecada4e831191d3185035e"
ARGS = ["--no-sandbox", "--allow-file-access-from-files", "--disable-gpu"]
if POLICY:
    ARGS += [f"--hatch-webgl-allowed-domains-file={POLICY}",
             f"--hatch-webgl-allowed-domains-sha256={SHA}"]

mode = sys.argv[1] if len(sys.argv) > 1 else "stills"
(base / "stills_long").mkdir(exist_ok=True)
(base / "frames_long").mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("CHROME_PATH", "/opt/meta-chromium/chrome"), args=ARGS)
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(f"file://{base}/long.html")
    pg.wait_for_function("window.__ready === true")
    pg.evaluate("document.fonts.ready.then(()=>{window.__fonts=true})")
    pg.wait_for_function("window.__fonts === true")
    pg.evaluate("Promise.all([document.fonts.load('64px BVPBlack'), document.fonts.load('30px BVPXBold'), document.fonts.load('24px BVPSemi')]).then(()=>{window.__fl=true})")
    pg.wait_for_function("window.__fl === true")
    pg.wait_for_timeout(500)
    if mode == "stills":
        for t in [3.6, 14.0, 24.0, 33.0, 42.0, 52.0, 60.0, 66.5]:
            pg.evaluate(f"window.render({t})")
            pg.wait_for_timeout(120)
            out = base / "stills_long" / f"t{t}.png"
            pg.screenshot(path=str(out))
            print("still", out, flush=True)
    else:
        frames = base / "frames_long"
        total = 2040
        for i in range(total):
            fn = frames / f"f{i:04d}.jpg"
            if not fn.exists():
                pg.evaluate(f"window.render({i/30})")
                pg.screenshot(path=str(fn), type="jpeg", quality=82)
            if i % 150 == 0:
                print("frame", i, flush=True)
        print("CAPTURE_DONE", total, flush=True)
    b.close()
