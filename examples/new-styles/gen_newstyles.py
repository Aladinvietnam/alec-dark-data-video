import base64, json
from pathlib import Path

base = Path(__file__).parent
import os
fonts_dir = Path(os.environ.get("ALEC_FONT_DIR", "fonts"))

def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()

geo = json.loads(Path(os.environ.get("ALEC_GEOJSON", "countries.geojson")).read_text())
world = []
for f in geo["features"]:
    g = f["geometry"]
    if not g:
        continue
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in polys:
        ring = poly[0]
        pts = [[round(x, 1), round(y, 1)] for x, y in ring[::2]]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx = sum(xs) / len(xs); cy = sum(ys) / len(ys)
        world.append({"p": pts, "c": [round(cx, 1), round(cy, 1)]})
world_js = json.dumps(world)

html = r"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{ font-family:'BVPBlack'; src:url(data:font/ttf;base64,__BLACK__) format('truetype'); }
@font-face{ font-family:'BVPXBold'; src:url(data:font/ttf;base64,__XBOLD__) format('truetype'); }
@font-face{ font-family:'BVPSemi'; src:url(data:font/ttf;base64,__SEMI__) format('truetype'); }
@font-face{ font-family:'PlexMono'; src:url(data:font/ttf;base64,__MONO__) format('truetype'); }
html,body{ margin:0; background:#000; } canvas{ display:block; }
</style></head><body>
<canvas id="cv" width="1920" height="1080"></canvas>
<script>
const WORLD = __WORLD__;
const x = document.getElementById('cv').getContext('2d');
const W = 1920, H = 1080;
const GOLD = '#E8B33C', RED = '#FF2E4D', TEAL = '#2BD9E8', WHITE = '#F4F6FA', GREY = '#8E9BAE';
function clamp(v,a,b){ return Math.max(a, Math.min(b, v)); }
function fade(t,a,b){ return clamp((t-a)/Math.max(0.0001, b-a), 0, 1); }
function eo(p){ return 1 - Math.pow(1-p, 3); }
function eob(p){ const c = 1.70158; return 1 + (c+1)*Math.pow(p-1,3) + c*Math.pow(p-1,2); }
function rr(c, px, py, w, h, r){ c.beginPath(); c.moveTo(px+r,py); c.arcTo(px+w,py,px+w,py+h,r); c.arcTo(px+w,py+h,px,py+h,r); c.arcTo(px,py+h,px,py,r); c.arcTo(px,py,px+w,py,r); c.closePath(); }
function text(str, tx, ty, size, font, color, align, alpha, ls){
  x.save(); x.globalAlpha = alpha === undefined ? 1 : alpha; x.fillStyle = color;
  x.font = size + 'px ' + font; x.textAlign = align || 'left'; x.textBaseline = 'alphabetic';
  try{ x.letterSpacing = (ls || 0) + 'px'; }catch(e){}
  x.fillText(str, tx, ty); x.restore();
}
function tw(str, size, font){ x.save(); x.font = size + 'px ' + font; const w = x.measureText(str).width; x.restore(); return w; }
function wproj(lon, lat){ return [90 + (lon+180)/360*1740, 120 + (82-lat)/150*800]; }
let seed = 11; function rnd(){ seed = (seed*16807) % 2147483647; return seed / 2147483647; }
function flameAt(cx, cy, s, t, seedv){
  const wob = Math.sin(t*11 + seedv) * 0.07;
  x.save(); x.translate(cx, cy); x.scale(s*(1+wob), s*(1-wob));
  const g = x.createLinearGradient(0, 14, 0, -20);
  g.addColorStop(0, '#FF5A2A'); g.addColorStop(0.6, '#FF8A2A'); g.addColorStop(1, '#FFC21A');
  x.fillStyle = g; x.beginPath();
  x.moveTo(0, -20); x.bezierCurveTo(9, -8, 11, 2, 8, 9); x.bezierCurveTo(5, 15, -5, 15, -8, 9); x.bezierCurveTo(-11, 2, -7, -6, 0, -20); x.fill();
  x.fillStyle = '#FFE98A'; x.beginPath();
  x.moveTo(0, -6); x.bezierCurveTo(4.5, 0, 5, 5, 3, 9); x.bezierCurveTo(1, 12, -3, 11, -4, 7); x.bezierCurveTo(-5, 2, -3, -2, 0, -6); x.fill();
  x.restore();
}
/* ---------- 0 · BORDER FLOOD ---------- */
function s_flood(lt){
  x.fillStyle = '#0A0F1C'; x.fillRect(0, 0, W, H);
  const R = 6 + eo(fade(lt, 0.4, 4.8)) * 46;
  WORLD.forEach(P => {
    const d = Math.hypot(P.c[0] - 31, P.c[1] - 41);
    x.beginPath();
    P.p.forEach((pt, i) => { const q = wproj(pt[0], pt[1]); i ? x.lineTo(q[0], q[1]) : x.moveTo(q[0], q[1]); });
    x.closePath();
    if(d < R){ x.fillStyle = 'rgba(232,160,60,0.85)'; x.fill(); }
    else { x.fillStyle = '#182238'; x.fill(); }
    x.strokeStyle = 'rgba(140,170,220,0.16)'; x.lineWidth = 1; x.stroke();
  });
  const caps = [[31,41,'CONSTANTINOPLE',16,-16,'left'],[23,40,'ATHENS',-16,6,'right'],[35,33,'DAMASCUS',16,6,'left'],[31,30,'CAIRO',0,32,'center'],[44,33,'BAGHDAD',16,-12,'left']];
  caps.forEach(c => {
    const d = Math.hypot(c[0] - 31, c[1] - 41);
    if(R > d){
      const q = wproj(c[0], c[1]); const pop = eob(fade(lt, 0.4 + (d/46)*4.4, 0.75 + (d/46)*4.4));
      x.save(); x.translate(q[0], q[1]); x.scale(Math.max(0.01, pop), Math.max(0.01, pop));
      x.fillStyle = '#FFF3D6'; x.beginPath(); x.arc(0, 0, 7, 0, Math.PI*2); x.fill(); x.restore();
      text(c[2], q[0] + c[3], q[1] + c[4], 19, 'BVPXBold', '#FFE1A0', c[5], 1, 1);
    }
  });
  text('ONE COLOUR TAKES THE MAP', 64, 92, 40, 'BVPBlack', WHITE, 'left', 1, 1);
  const year = 1400 + Math.floor(eo(fade(lt, 0.4, 4.8)) * 120 + Math.max(0, lt - 0.4) * 2);
  text(String(Math.min(1520, year)), 1856, 1006, 120, 'BVPBlack', GOLD, 'right', 1, 0);
  text('YEAR', 1856, 912, 24, 'BVPXBold', GREY, 'right', 1, 4);
}
/* ---------- 1 · CHAT THREAD ---------- */
function s_chat(lt){
  const g = x.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, '#101623'); g.addColorStop(1, '#070A12'); x.fillStyle = g; x.fillRect(0, 0, W, H);
  text('TOLD AS A CONVERSATION', 90, 300, 44, 'BVPBlack', WHITE, 'left', 1, 1);
  text('every bubble is a cliffhanger', 90, 356, 28, 'BVPSemi', GREY, 'left', 1, 0);
  text('the typing dots do the suspense', 90, 402, 28, 'BVPSemi', GREY, 'left', 1, 0);
  const px = 1180, pw = 560;
  x.save(); x.shadowColor = 'rgba(0,0,0,0.6)'; x.shadowBlur = 40;
  x.fillStyle = '#0B141A'; rr(x, px, 90, pw, 900, 36); x.fill(); x.restore();
  x.save(); rr(x, px, 90, pw, 900, 36); x.clip();
  x.fillStyle = '#1F2C34'; x.fillRect(px, 90, pw, 96);
  x.fillStyle = '#5B6B76'; x.beginPath(); x.arc(px + 52, 138, 26, 0, Math.PI*2); x.fill();
  text('?', px + 52, 148, 30, 'BVPBlack', '#0B141A', 'center', 1, 0);
  text('Unknown Number', px + 92, 132, 25, 'BVPXBold', WHITE, 'left', 1, 0);
  text('online', px + 92, 164, 20, 'BVPSemi', '#3ECF6E', 'left', 1, 0);
  text('3:12 AM', px + pw/2, 226, 19, 'BVPSemi', '#7A8A94', 'center', 1, 1);
  const MSGS = [
    { side: 0, txt: 'are you awake?', at: 0.3 },
    { side: 1, txt: 'it is 3am. what happened', at: 1.0 },
    { side: 0, txt: 'someone is in the garden', at: 1.8 },
    { side: 0, txt: 'they are standing at your window', at: 3.0 },
    { side: 1, txt: 'WHAT', at: 3.7 },
    { side: 0, txt: 'do not turn around.', at: 4.5, hot: 1 }
  ];
  let by = 268;
  const rows = [];
  MSGS.forEach(m => {
    const wdt = Math.min(424, tw(m.txt, 22, 'BVPSemi') + 38);
    rows.push({ m, w: wdt, y: by }); by += 74;
  });
  rows.forEach(r => {
    if(lt < r.m.at) return;
    const pop = eob(fade(lt, r.m.at, r.m.at + 0.3));
    const bx = r.m.side ? px + pw - 28 - r.w : px + 28;
    x.save(); x.translate(bx + r.w/2, r.y + 26); x.scale(Math.max(0.01, pop), Math.max(0.01, pop)); x.translate(-(bx + r.w/2), -(r.y + 26));
    x.fillStyle = r.m.side ? '#005C4B' : '#1F2C34'; rr(x, bx, r.y, r.w, 52, 14); x.fill();
    text(r.m.txt, bx + 18, r.y + 34, 22, 'BVPSemi', r.m.hot ? '#FF8A7A' : '#E8EDEF', 'left', 1, 0);
    x.restore();
  });
  if(lt > 2.25 && lt < 3.0){
    const bx = px + 28;
    x.fillStyle = '#1F2C34'; rr(x, bx, 268 + 74*3, 84, 52, 14); x.fill();
    for(let k = 0; k < 3; k++){
      const ph = 0.5 + 0.5 * Math.sin(lt * 10 - k * 1.1);
      x.fillStyle = 'rgba(220,230,235,' + (0.35 + 0.55 * ph) + ')';
      x.beginPath(); x.arc(bx + 22 + k * 20, 268 + 74*3 + 26 - ph * 3, 5, 0, Math.PI*2); x.fill();
    }
  }
  x.restore();
  x.strokeStyle = 'rgba(255,255,255,0.14)'; x.lineWidth = 2; rr(x, px, 90, pw, 900, 36); x.stroke();
}
/* ---------- 2 · CASE FILE ---------- */
function s_case(lt){
  x.fillStyle = '#0A0A0C'; x.fillRect(0, 0, W, H);
  text('SHE VANISHED IN BROAD DAYLIGHT', 64, 96, 42, 'BVPBlack', WHITE, 'left', 1, 1);
  text('HOOK LINE NEVER LEAVES THE TOP', 64, 140, 20, 'BVPXBold', RED, 'left', 1, 3);
  function photo(cx, cy, w, h, rot, kind, label){
    x.save(); x.translate(cx, cy); x.rotate(rot);
    const kb = 1 + 0.05 * fade(lt, 0, 5.5);
    x.scale(kb, kb);
    x.fillStyle = '#E8E4DA'; x.fillRect(-w/2 - 10, -h/2 - 10, w + 20, h + 46);
    const gg = x.createLinearGradient(0, -h/2, 0, h/2);
    if(kind === 0){ gg.addColorStop(0, '#3A4356'); gg.addColorStop(1, '#141A26'); }
    if(kind === 1){ gg.addColorStop(0, '#2E3A2E'); gg.addColorStop(1, '#10160F'); }
    if(kind === 2){ gg.addColorStop(0, '#4A3A34'); gg.addColorStop(1, '#1C130E'); }
    x.fillStyle = gg; x.fillRect(-w/2, -h/2, w, h);
    if(kind === 0){
      x.fillStyle = '#0A0D14'; x.fillRect(-90, -30, 180, 130);
      x.beginPath(); x.moveTo(-110, -30); x.lineTo(0, -95); x.lineTo(110, -30); x.closePath(); x.fill();
      x.fillStyle = '#FFD98A'; x.fillRect(-24, 18, 48, 52);
    }
    if(kind === 1){
      x.strokeStyle = 'rgba(255,120,90,0.9)'; x.lineWidth = 5; x.setLineDash([12, 9]);
      x.beginPath(); x.moveTo(-w/2 + 30, h/2 - 30); x.quadraticCurveTo(0, -h/2 + 40, w/2 - 40, -h/2 + 70); x.stroke(); x.setLineDash([]);
      x.fillStyle = RED; x.beginPath(); x.arc(w/2 - 40, -h/2 + 70, 10, 0, Math.PI*2); x.fill();
    }
    if(kind === 2){
      x.fillStyle = '#0D0B09'; x.beginPath(); x.arc(0, -28, 44, 0, Math.PI*2); x.fill();
      x.beginPath(); x.ellipse(0, 96, 74, 62, 0, Math.PI, 0); x.fill();
    }
    text(label, 0, h/2 + 32, 20, 'PlexMono', '#3A362E', 'center', 1, 1);
    x.restore();
  }
  photo(430, 470, 460, 320, -0.03, 0, 'THE HOUSE · LAST PHOTO 14:02');
  photo(1010, 430, 420, 300, 0.025, 1, 'ROUTE THAT AFTERNOON');
  photo(1520, 500, 380, 300, -0.02, 2, 'THE ONLY WITNESS');
  x.strokeStyle = 'rgba(255,46,77,0.75)'; x.lineWidth = 3;
  x.beginPath(); x.moveTo(660, 380); x.lineTo(820, 350); x.stroke();
  x.beginPath(); x.moveTo(1210, 380); x.lineTo(1340, 430); x.stroke();
  x.fillStyle = GOLD; [[660,380],[820,350],[1210,380],[1340,430]].forEach(p => { x.beginPath(); x.arc(p[0], p[1], 8, 0, Math.PI*2); x.fill(); });
  const facts = ['NAME AND DATE STAMP THEMSELVES IN', 'EVERY STILL PUSHES IN, NOTHING IS STATIC', 'THE TWIST LANDS BEFORE SECOND 45'];
  facts.forEach((f, i) => { if(lt > 1 + i * 1.1) text(f, 64, 880 + i * 52, 26, 'BVPXBold', '#C9CDD6', 'left', fade(lt, 1 + i * 1.1, 1.3 + i * 1.1), 1); });
  if(lt > 4.2){
    const p = fade(lt, 4.2, 4.45); const sc = 2 - eo(p);
    x.save(); x.translate(960, 660); x.rotate(-0.1); x.scale(sc, sc); x.globalAlpha = p;
    x.strokeStyle = RED; x.lineWidth = 6; rr(x, -270, -58, 540, 116, 10); x.stroke();
    text('STILL UNSOLVED', 0, 30, 62, 'BVPBlack', RED, 'center', 1, 2);
    x.restore();
  }
}
/* ---------- 3 · BAR RACE ---------- */
const RACE = [
  { n: 'NOKIA', c: '#4A90D9', a: 290, b: 12 }, { n: 'KODAK', c: '#B0B7C3', a: 180, b: 2 },
  { n: 'SONY', c: '#7A6FD0', a: 210, b: 95 }, { n: 'APPLE', c: '#E8E8EC', a: 90, b: 380 },
  { n: 'SAMSUNG', c: '#3ECF6E', a: 120, b: 240 }, { n: 'XIAOMI', c: '#FF8A3C', a: 4, b: 150 },
  { n: 'TESLA', c: '#FF2E4D', a: 6, b: 210 }
];
let raceY = null;
function s_race(lt){
  x.fillStyle = '#0A0E18'; x.fillRect(0, 0, W, H);
  text('THE RANKING IS THE STORY', 64, 92, 40, 'BVPBlack', WHITE, 'left', 1, 1);
  const p = eo(fade(lt, 0.3, 4.9));
  const vals = RACE.map(r => ({ r, v: r.a + (r.b - r.a) * p }));
  const order = [...vals].sort((m, n) => n.v - m.v);
  if(!raceY) raceY = RACE.map((r, i) => 190 + i * 118);
  order.forEach((o, rank) => {
    const idx = RACE.indexOf(o.r); const target = 190 + rank * 118;
    raceY[idx] += (target - raceY[idx]) * 0.2;
    const y = raceY[idx]; const wdt = 120 + (o.v / 400) * 1380;
    x.fillStyle = o.r.c; rr(x, 300, y, wdt, 74, 8); x.fill();
    text(o.r.n, 280, y + 50, 28, 'BVPXBold', WHITE, 'right', 1, 1);
    text('$' + Math.round(o.v) + 'B', 316 + wdt, y + 50, 30, 'BVPBlack', o.r.c, 'left', 1, 0);
  });
  const yr = 2007 + Math.round(p * 18);
  text(String(yr), 1856, 1006, 110, 'BVPBlack', GOLD, 'right', 1, 0);
}
/* ---------- 4 · MONEY RIVER ---------- */
function s_river(lt){
  x.fillStyle = '#070B14'; x.fillRect(0, 0, W, H);
  text('WHERE THE MONEY ACTUALLY GOES', 64, 92, 40, 'BVPBlack', WHITE, 'left', 1, 1);
  const flows = [
    { n: 'COST OF GOODS', share: 0.52, c: '#5B7FB0' }, { n: 'RESEARCH', share: 0.09, c: '#7A6FD0' },
    { n: 'MARKETING', share: 0.07, c: '#3E8FB0' }, { n: 'TAX', share: 0.10, c: '#B08A3E' },
    { n: 'PROFIT', share: 0.22, c: '#2FBF71' }
  ];
  const sx = 330, sy0 = 300, totalH = 470;
  x.fillStyle = '#22314E'; rr(x, 90, sy0, 190, totalH, 12); x.fill();
  text('REVENUE', 185, sy0 - 24, 24, 'BVPXBold', WHITE, 'center', 1, 2);
  text('$412B', 185, sy0 + totalH/2 + 16, 44, 'BVPBlack', GOLD, 'center', 1, 0);
  let acc = 0;
  flows.forEach((f, i) => {
    const h = f.share * totalH; const yTop = sy0 + acc; acc += h;
    const ty = 190 + i * 150; const th = Math.max(52, f.share * 560);
    const rev = fade(lt, 0.4 + i * 0.55, 1.5 + i * 0.55);
    if(rev > 0){
      x.save(); x.beginPath(); x.rect(0, 0, sx + 1120 * rev + 200, H); x.clip();
      x.beginPath();
      x.moveTo(sx, yTop);
      x.bezierCurveTo(sx + 420, yTop, 1290, ty, 1540, ty);
      x.lineTo(1540, ty + th);
      x.bezierCurveTo(1290, ty + th, sx + 420, yTop + h, sx, yTop + h);
      x.closePath();
      x.fillStyle = f.c; x.globalAlpha = 0.85; x.fill(); x.restore();
      const trav = (lt * 0.24 + i * 0.37) % 1;
      const qx = sx + (1540 - sx) * trav;
      const qy = (yTop + h/2) + (ty + th/2 - (yTop + h/2)) * trav * trav;
      x.save(); x.globalAlpha = rev; x.fillStyle = '#FFFFFF';
      x.beginPath(); x.arc(qx, qy, 5, 0, Math.PI*2); x.fill(); x.restore();
    }
    const amt = Math.round(412 * f.share * fade(lt, 0.9 + i * 0.55, 2 + i * 0.55));
    const slotY = 246 + i * 138;
    x.fillStyle = f.c; x.fillRect(1546, ty, 10, th);
    text(f.n, 1580, slotY, 25, 'BVPXBold', WHITE, 'left', fade(lt, 0.6 + i * 0.55, 1 + i * 0.55), 1);
    text('$' + amt + 'B', 1580, slotY + 36, 27, 'BVPBlack', f.c, 'left', fade(lt, 0.9 + i * 0.55, 1.3 + i * 0.55), 0);
  });
}
/* ---------- 5 · RISE AND FALL ---------- */
function s_risefall(lt){
  x.fillStyle = '#0A0C12'; x.fillRect(0, 0, W, H);
  const fall = lt > 3.4;
  text(fall ? 'ACT II · THE FALL' : 'ACT I · THE RISE', 64, 96, 34, 'BVPBlack', fall ? RED : GOLD, 'left', fade(lt, 0.1, 0.3) * (fall ? fade(lt, 3.4, 3.6) : 1), 2);
  const pts = [[140,880],[420,790],[700,640],[980,470],[1180,330],[1330,268],[1460,300],[1560,760],[1660,880],[1790,906]];
  const total = pts.length - 1; const prog = fade(lt, 0.3, 5.0) * total;
  x.save(); x.strokeStyle = fall && prog > 6 ? RED : GOLD; x.lineWidth = 6; x.lineJoin = 'round'; x.shadowColor = x.strokeStyle; x.shadowBlur = 12;
  x.beginPath();
  for(let i = 0; i <= Math.floor(prog); i++){ i ? x.lineTo(pts[i][0], pts[i][1]) : x.moveTo(pts[i][0], pts[i][1]); }
  const fr = prog - Math.floor(prog);
  if(Math.floor(prog) < total){
    const a = pts[Math.floor(prog)], b = pts[Math.floor(prog) + 1];
    x.lineTo(a[0] + (b[0] - a[0]) * fr, a[1] + (b[1] - a[1]) * fr);
  }
  x.stroke(); x.restore();
  const eras = [[420, 700, 'FOUNDED · 2007', 0.8], [980, 380, 'IPO · 2012', 1.9], [1330, 178, 'PEAK · $68B', 2.9], [1660, 700, 'BANKRUPT · 2024', 4.3]];
  eras.forEach(e => {
    if(lt > e[3]){
      x.fillStyle = e[3] > 4 ? RED : GOLD; x.beginPath(); x.arc(e[0], e[1] + 60, 8, 0, Math.PI*2); x.fill();
      text(e[2], e[0], e[1], 25, 'BVPXBold', WHITE, 'center', fade(lt, e[3], e[3] + 0.3), 1);
    }
  });
  const val = prog < 5 ? Math.round(68 * (prog / 5)) : (prog < 6.4 ? 68 : Math.max(0, Math.round(68 - (prog - 6.4) * 60)));
  text('$' + val + 'B', 1790, 120, 64, 'BVPBlack', fall ? RED : GOLD, 'right', 1, 0);
  text('MARKET VALUE', 1790, 66, 20, 'BVPXBold', GREY, 'right', 1, 3);
}
</script></body></html>"""

html = (html.replace("__BLACK__", b64(fonts_dir / "BeVietnamPro-Black.ttf"))
            .replace("__XBOLD__", b64(fonts_dir / "BeVietnamPro-ExtraBold.ttf"))
            .replace("__SEMI__", b64(fonts_dir / "BeVietnamPro-SemiBold.ttf"))
            .replace("__MONO__", b64(fonts_dir / "IBMPlexMono-Bold.ttf"))
            .replace("__WORLD__", world_js))
(base / "newstyles_part1.html").write_text(html)
print("part1 bytes", len(html))
