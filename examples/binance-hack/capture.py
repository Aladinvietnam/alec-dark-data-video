import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

base = Path(__file__).parent
import os
ARGS = ["--no-sandbox", "--allow-file-access-from-files", "--disable-gpu"]
CHROME = os.environ.get("CHROME_PATH") or None

mode = sys.argv[1] if len(sys.argv) > 1 else "stills"
(base / "stills").mkdir(exist_ok=True)
(base / "frames").mkdir(exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=ARGS)
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(f"file://{base}/scene.html")
    pg.wait_for_function("window.__ready === true")
    pg.evaluate("document.fonts.ready.then(()=>{window.__fonts=true})")
    pg.wait_for_function("window.__fonts === true")
    if mode == "stills":
        for t in [2.0, 12.0, 18.0, 22.0, 26.0, 34.5]:
            pg.evaluate(f"window.render({t})")
            out = base / "stills" / f"t{t}.png"
            pg.screenshot(path=str(out))
            print("still", out, flush=True)
    else:
        frames = base / "frames"
        total = 1062
        for i in range(total):
            fn = frames / f"f{i:04d}.jpg"
            if not fn.exists():
                pg.evaluate(f"window.render({i/30})")
                pg.screenshot(path=str(fn), type="jpeg", quality=82)
            if i % 120 == 0:
                print("frame", i, flush=True)
        print("CAPTURE_DONE", total, flush=True)
    b.close()
