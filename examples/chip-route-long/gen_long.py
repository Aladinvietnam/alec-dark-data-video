import base64, json
from pathlib import Path

base = Path(__file__).parent
import os
fonts_dir = Path(os.environ.get("ALEC_FONT_DIR", "/home/hatch/workspace/ban_tin_29_10/short/fonts"))

def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()

geo = json.loads((base / "countries.geojson").read_text())
polys = []
for f in geo["features"]:
    g = f["geometry"]
    if not g:
        continue
    rings_list = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    for poly in rings_list:
        ring = poly[0]
        pts = [[round(x, 1), round(y, 1)] for x, y in ring[::2]]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        polys.append({"b": [min(xs), min(ys), max(xs), max(ys)], "p": pts})
geo_js = json.dumps(polys)

html = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{ font-family:'BVPBlack'; src:url(data:font/ttf;base64,__BLACK__) format('truetype'); }
@font-face{ font-family:'BVPXBold'; src:url(data:font/ttf;base64,__XBOLD__) format('truetype'); }
@font-face{ font-family:'BVPSemi'; src:url(data:font/ttf;base64,__SEMI__) format('truetype'); }
html,body{ margin:0; background:#070A1E; } canvas{ display:block; }
</style></head><body>
<canvas id="cv" width="1920" height="1080"></canvas>
<script>
const POLYS = __GEO__;
const SRC = __IMGSRC__;
const IMGS = {};
['fab', 'euv', 'dc', 'strait'].forEach(k => {
  const im = new Image();
  im.src = SRC[k];
  IMGS[k] = im;
});
const x = document.getElementById('cv').getContext('2d');
const W = 1920, H = 1080, DUR = 68.0;
const B1 = 9.2, B2 = 19.0, B3 = 28.8, B4 = 36.4, B5 = 46.9, B6 = 56.2;
const GOLD = '#FFC21A', GOLDL = '#FFDF4D', RED = '#FF4A3D', TEAL = '#2BD9A9', WHITE = '#F7F5EF', GREY = '#A7B0BA';
function clamp(v,a,b){ return Math.max(a, Math.min(b, v)); }
function fade(t,a,b){ return clamp((t-a)/Math.max(0.0001, b-a), 0, 1); }
function eo(p){ return 1 - Math.pow(1-p, 3); }
function smooth(p){ return p*p*(3-2*p); }
function rr(c, px, py, w, h, r){ c.beginPath(); c.moveTo(px+r,py); c.arcTo(px+w,py,px+w,py+h,r); c.arcTo(px+w,py+h,px,py+h,r); c.arcTo(px,py+h,px,py,r); c.arcTo(px,py,px+w,py,r); c.closePath(); }
function text(str, tx, ty, size, font, color, align, alpha, ls){
  x.save(); x.globalAlpha = alpha; x.fillStyle = color;
  x.font = size + 'px ' + font; x.textAlign = align; x.textBaseline = 'alphabetic';
  try{ x.letterSpacing = ls + 'px'; }catch(e){}
  x.fillText(str, tx, ty); x.restore();
}
function tw(str, size, font){ x.save(); x.font = size + 'px ' + font; const w = x.measureText(str).width; x.restore(); return w; }
function fitSize(str, maxW, size, font){
  let s = size;
  while(s > 10 && tw(str, s, font) > maxW) s -= 2;
  return s;
}
function blob(bx, by, r, rgba, a){
  const g = x.createRadialGradient(bx, by, 0, bx, by, r);
  g.addColorStop(0, rgba.replace('A', a)); g.addColorStop(1, rgba.replace('A', '0'));
  x.fillStyle = g; x.fillRect(bx-r, by-r, r*2, r*2);
}
let seed = 11; function rnd(){ seed = (seed*16807) % 2147483647; return seed / 2147483647; }
const STARS = []; for(let i=0;i<110;i++){ STARS.push({ sx: rnd()*1920, sy: rnd()*1080, sr: rnd()*1.7+0.5, sa: rnd()*0.17+0.06 }); }
function bg(t){
  const g = x.createLinearGradient(0,0,1920,1080);
  g.addColorStop(0,'#182259'); g.addColorStop(0.5,'#10173F'); g.addColorStop(1,'#080C22');
  x.fillStyle = g; x.fillRect(0,0,W,H);
  blob(430 + 40*Math.sin(t*0.10), 190 + 26*Math.cos(t*0.08), 680, 'rgba(139,63,255,A)', 0.34);
  blob(1500 + 46*Math.cos(t*0.07), 130, 560, 'rgba(46,116,255,A)', 0.28);
  blob(1640, 900 + 30*Math.cos(t*0.09), 740, 'rgba(16,212,178,A)', 0.24);
  blob(960, 1010, 620, 'rgba(224,64,251,A)', 0.15);
  x.fillStyle = '#FFFFFF';
  STARS.forEach(s => { x.save(); x.globalAlpha = s.sa; x.beginPath(); x.arc(s.sx, s.sy, s.sr, 0, Math.PI*2); x.fill(); x.restore(); });
}
function vignette(){
  const v = x.createRadialGradient(960, 540, 520, 960, 540, 1080);
  v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,0.38)');
  x.fillStyle = v; x.fillRect(0,0,W,H);
}
function proj(lon, lat){ return [120 + (lon+180)/360*1680, 226 + (78-lat)/136*660]; }
function inRing(px, py, ring){
  let inside = false;
  for(let i=0, j=ring.length-1; i<ring.length; j=i++){
    const xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
    if(((yi>py) !== (yj>py)) && (px < (xj-xi)*(py-yi)/(yj-yi)+xi)) inside = !inside;
  }
  return inside;
}
function onLand(lon, lat){
  for(const P of POLYS){
    const b = P.b;
    if(lon < b[0] || lon > b[2] || lat < b[1] || lat > b[3]) continue;
    if(inRing(lon, lat, P.p)) return true;
  }
  return false;
}
function invWorld(gx, gy){ return [(gx-120)/1680*360-180, 78-(gy-226)/660*136]; }
function dotMap(alpha){
  for(let gx=120; gx<=1800; gx+=13){
    for(let gy=226; gy<=886; gy+=13){
      const ll = invWorld(gx, gy);
      if(onLand(ll[0], ll[1])){
        x.fillStyle = 'rgba(178,192,255,' + alpha + ')';
        x.beginPath(); x.arc(gx, gy, 2.3, 0, Math.PI*2); x.fill();
      }
    }
  }
}
const CAMK = [
  [0.0, 1400, 490, 1.25], [2.4, 1527, 483, 2.05], [8.8, 1527, 483, 2.05],
  [10.4, 960, 545, 1.0], [28.8, 960, 545, 1.0],
  [30.4, 700, 500, 1.25], [36.0, 700, 500, 1.25],
  [37.6, 1518, 484, 1.9], [46.5, 1518, 484, 1.9],
  [48.1, 1100, 520, 1.12], [55.8, 1100, 520, 1.12],
  [57.4, 960, 545, 1.0], [68.0, 960, 545, 1.03]
];
function cam(t){
  for(let i=0;i<CAMK.length-1;i++){
    const a = CAMK[i], b = CAMK[i+1];
    if(t >= a[0] && t <= b[0]){
      const p = smooth(fade(t, a[0], b[0]));
      return [a[1]+(b[1]-a[1])*p, a[2]+(b[2]-a[2])*p, a[3]+(b[3]-a[3])*p];
    }
  }
  const l = CAMK[CAMK.length-1];
  return [l[1], l[2], l[3]];
}
function bez(p0, p1, p2, u){
  const a = (1-u)*(1-u), b = 2*(1-u)*u, c = u*u;
  return [a*p0[0] + b*p1[0] + c*p2[0], a*p0[1] + b*p1[1] + c*p2[1]];
}
function drawBez(p0, p1, p2, prog, color, width){
  if(prog <= 0) return;
  x.save(); x.strokeStyle = color; x.lineWidth = width;
  x.shadowColor = color; x.shadowBlur = 18;
  x.beginPath();
  const upto = Math.max(2, Math.ceil(60 * prog));
  for(let i=0;i<=upto;i++){
    const q = bez(p0, p1, p2, prog * i / upto);
    i ? x.lineTo(q[0], q[1]) : x.moveTo(q[0], q[1]);
  }
  x.stroke(); x.restore();
}
function glass(px, py, w, h, accent){
  x.save(); x.shadowColor = 'rgba(0,0,0,0.45)'; x.shadowBlur = 26; x.shadowOffsetY = 10;
  x.fillStyle = 'rgba(13,18,42,0.9)'; rr(x, px, py, w, h, 16); x.fill(); x.restore();
  x.strokeStyle = 'rgba(255,255,255,0.15)'; x.lineWidth = 1; rr(x, px, py, w, h, 16); x.stroke();
  if(accent){ x.fillStyle = accent; rr(x, px, py+22, 5, h-44, 2); x.fill(); }
}
function subtitle(str, s0, s1, t){
  const a = Math.min(fade(t, s0, s0+0.35), 1 - fade(t, s1-0.3, s1));
  if(a <= 0) return;
  const fs = fitSize(str, 1480, 30, 'BVPSemi');
  const wch = tw(str, fs, 'BVPSemi') + 64;
  x.save(); x.globalAlpha = a;
  x.fillStyle = 'rgba(7,9,24,0.88)'; rr(x, 960-wch/2, 988, wch, 62, 31); x.fill();
  x.strokeStyle = 'rgba(255,255,255,0.16)'; x.lineWidth = 1; rr(x, 960-wch/2, 988, wch, 62, 31); x.stroke();
  text(str, 960, 1029, fs, 'BVPSemi', WHITE, 'center', 1, 0);
  x.restore();
}
function imgPanel(key, caption, t0, t1, t){
  const a = Math.min(fade(t, t0, t0+0.8), 1 - fade(t, t1-0.5, t1));
  if(a <= 0) return;
  const slide = (1 - eo(fade(t, t0, t0+0.8))) * 80;
  const px = 1170 + slide, py = 292, pw = 640, ph = 368;
  const img = IMGS[key];
  x.save(); x.globalAlpha = a;
  x.shadowColor = 'rgba(0,0,0,0.5)'; x.shadowBlur = 28; x.shadowOffsetY = 10;
  rr(x, px, py, pw, ph, 16); x.clip();
  if(img && img.naturalWidth){
    const sc = Math.max(pw/img.naturalWidth, ph/img.naturalHeight);
    const dw = img.naturalWidth*sc, dh = img.naturalHeight*sc;
    x.drawImage(img, px + (pw-dw)/2, py + (ph-dh)/2, dw, dh);
  } else { x.fillStyle = '#141B3D'; x.fillRect(px, py, pw, ph); }
  const g = x.createLinearGradient(0, py+ph-130, 0, py+ph);
  g.addColorStop(0, 'rgba(5,7,18,0)'); g.addColorStop(1, 'rgba(5,7,18,0.88)');
  x.fillStyle = g; x.fillRect(px, py+ph-130, pw, 130);
  x.restore();
  x.save(); x.globalAlpha = a;
  x.strokeStyle = 'rgba(255,255,255,0.22)'; x.lineWidth = 1; rr(x, px, py, pw, ph, 16); x.stroke();
  text(caption, px+26, py+ph-24, 24, 'BVPXBold', WHITE, 'left', 1, 2);
  const il = 'ILLUSTRATION';
  const iw = tw(il, 16, 'BVPXBold') + 68;
  x.fillStyle = 'rgba(7,9,24,0.8)'; rr(x, px+pw-iw-16, py+16, iw, 32, 16); x.fill();
  text(il, px+pw-iw/2-16, py+38, 16, 'BVPXBold', GREY, 'center', 1, 2);
  x.restore();
}
function statBlock(t0, t1, t, big, bigColor, line1, line2){
  const a = Math.min(fade(t, t0, t0+0.6), 1 - fade(t, t1-0.4, t1));
  if(a <= 0) return;
  text(line1, 110, 796, 26, 'BVPXBold', GREY, 'left', a, 2);
  text(big, 104, 902, 104, 'BVPBlack', bigColor, 'left', a, 0);
  text(line2, 110, 950, 24, 'BVPSemi', GREY, 'left', a, 1);
}
const TAI = proj(121.5, 25.0), AMS = proj(4.9, 52.4), SV = proj(-122.4, 37.8);
const NEWF = [
  [proj(-112, 33), 'ARIZONA · USA', B6+1.3, 'below'],
  [proj(130.7, 32.8), 'KUMAMOTO · JAPAN', B6+2.3, 'above'],
  [proj(13.7, 51.05), 'DRESDEN · GERMANY', B6+3.3, 'right']
];
window.render = function(t){
  x.clearRect(0, 0, W, H);
  bg(t);
  const [cx, cy, cs] = cam(t);
  x.save(); x.translate(960, 540); x.scale(cs, cs); x.translate(-cx, -cy);
  dotMap(t >= B5 && t < B6 ? 0.13 : 0.28);
  // routes: taipei to amsterdam during B2, amsterdam to silicon valley during B3
  drawBez(TAI, [(TAI[0]+AMS[0])/2, Math.min(TAI[1], AMS[1]) - 130], AMS, fade(t, B2+1.2, B2+4.6), GOLD, 5);
  drawBez(AMS, [(AMS[0]+SV[0])/2, Math.min(AMS[1], SV[1]) - 170], SV, fade(t, B3+1.0, B3+4.0), GOLD, 5);
  // target rings on taiwan during hook and strait beats
  const ringWin = (t < B1 - 0.6) || (t >= B4 - 0.4 && t < B5);
  if(ringWin){
    const rp = t < B1 ? fade(t, 0.7, 1.5) : fade(t, B4+0.6, B4+1.4);
    const pulse = 1 + 0.03 * Math.sin(t * 5);
    [52, 35, 19].forEach((r0, i) => {
      const rad = r0 * (1.7 - 0.7 * eo(clamp(rp*1.3 - i*0.15, 0, 1))) * pulse;
      x.save(); x.strokeStyle = RED; x.globalAlpha = 0.95 - i*0.22; x.lineWidth = 3;
      x.beginPath(); x.arc(TAI[0], TAI[1], Math.max(4, rad), 0, Math.PI*2); x.stroke(); x.restore();
    });
    x.save(); x.strokeStyle = RED; x.lineWidth = 3;
    [[0,-1],[0,1],[-1,0],[1,0]].forEach(d => {
      x.beginPath();
      x.moveTo(TAI[0] + d[0]*46, TAI[1] + d[1]*46); x.lineTo(TAI[0] + d[0]*64, TAI[1] + d[1]*64);
      x.stroke();
    });
    x.fillStyle = RED; x.beginPath(); x.arc(TAI[0], TAI[1], 5, 0, Math.PI*2); x.fill();
    x.restore();
  }
  // stop markers
  const stops = [
    [TAI, 'TAIPEI', 'TSMC · TAIWAN', B1+0.6, 66],
    [AMS, 'AMSTERDAM', 'ASML · NETHERLANDS', B2+4.4, -48],
    [SV, 'SILICON VALLEY', 'AI DATA CENTERS', B3+3.8, -48]
  ];
  const focusIdx = t < B1 ? -1 : (t < B4 ? -1 : (t < B5 ? 0 : -1));
  stops.forEach((s, si) => {
    let a = fade(t, s[3], s[3]+0.5);
    if(cs > 1.3 && focusIdx >= 0 && si !== focusIdx) a *= 0.06;
    if(a <= 0) return;
    x.save(); x.globalAlpha = a;
    x.strokeStyle = 'rgba(255,194,26,0.5)'; x.lineWidth = 3;
    x.beginPath(); x.arc(s[0][0], s[0][1], 24, 0, Math.PI*2); x.stroke();
    x.fillStyle = GOLD; x.shadowColor = 'rgba(255,194,26,0.8)'; x.shadowBlur = 16;
    x.beginPath(); x.arc(s[0][0], s[0][1], 9, 0, Math.PI*2); x.fill();
    x.restore();
    text(s[1], s[0][0], s[0][1] + s[4], 27, 'BVPXBold', WHITE, 'center', a, 1);
    text(s[2], s[0][0], s[0][1] + s[4] + 34, 23, 'BVPXBold', GOLDL, 'center', a, 1);
  });
  // new fab markers, closing beat
  NEWF.forEach(n => {
    const a = fade(t, n[2], n[2]+0.5);
    if(a <= 0) return;
    const pr = 1 + 0.25 * Math.abs(Math.sin((t - n[2]) * 3));
    x.save(); x.globalAlpha = a;
    x.strokeStyle = TEAL; x.lineWidth = 3;
    x.beginPath(); x.arc(n[0][0], n[0][1], 20 * pr, 0, Math.PI*2); x.stroke();
    x.fillStyle = TEAL; x.shadowColor = 'rgba(43,217,169,0.85)'; x.shadowBlur = 14;
    x.beginPath(); x.arc(n[0][0], n[0][1], 8, 0, Math.PI*2); x.fill();
    x.restore();
    if(n[3] === 'below') text(n[1], n[0][0], n[0][1] + 58, 23, 'BVPXBold', WHITE, 'center', a, 1);
    else if(n[3] === 'right') text(n[1], n[0][0] + 36, n[0][1] + 8, 23, 'BVPXBold', WHITE, 'left', a, 1);
    else text(n[1], n[0][0], n[0][1] - 34, 23, 'BVPXBold', WHITE, 'center', a, 1);
  });
  x.restore();
  vignette();
  // header
  text('THE CHIP ROUTE', 110, 118, 56, 'BVPBlack', WHITE, 'left', 1, 1);
  const kickers = [
    [0, B1, 'THE CHOKEPOINT EVERY CHIP MUST PASS'],
    [B1, B2, 'STOP 01 · TAIWAN, WHERE CHIPS ARE BORN'],
    [B2, B3, 'STOP 02 · THE NETHERLANDS, THE MACHINE MAKER'],
    [B3, B4, 'STOP 03 · SILICON VALLEY, THE DESTINATION'],
    [B4, B5, 'THE STRAIT THAT CARRIES THE TRADE'],
    [B5, B6, 'WHY THIS CHAIN IS FRAGILE'],
    [B6, DUR, 'THE RACE TO DIVERSIFY']
  ];
  kickers.forEach(k => {
    const a = Math.min(fade(t, k[0]+0.1, k[0]+0.7), 1 - fade(t, k[1]-0.4, k[1]));
    if(a > 0) text(k[2], 110, 168, 30, 'BVPXBold', GOLD, 'left', a, 3);
  });
  const gw = x.createLinearGradient(110, 0, 1810, 0);
  gw.addColorStop(0, 'rgba(255,194,26,0.85)'); gw.addColorStop(0.35, 'rgba(255,194,26,0.25)'); gw.addColorStop(1, 'rgba(255,194,26,0)');
  x.fillStyle = gw; x.fillRect(110, 190, 1700, 2);
  const tag = 'LONG FORM · FIGURES WITH SOURCES IN DESCRIPTION';
  const twd = tw(tag, 19, 'BVPXBold') + 36;
  x.fillStyle = 'rgba(10,14,34,0.85)'; rr(x, 1810-twd, 66, twd, 42, 21); x.fill();
  x.strokeStyle = 'rgba(255,255,255,0.25)'; x.lineWidth = 1; rr(x, 1810-twd, 66, twd, 42, 21); x.stroke();
  text(tag, 1810-twd/2, 94, 19, 'BVPXBold', GREY, 'center', 1, 2);
  // hook beat numbers
  if(t < B1){
    const hv = Math.round(90 * eo(fade(t, 1.2, 3.4)));
    text('OF THE WORLD’S MOST ADVANCED CHIPS', 110, 730, 26, 'BVPXBold', GREY, 'left', fade(t, 0.9, 1.4), 2);
    text(hv + '%', 104, 846, 118, 'BVPBlack', RED, 'left', fade(t, 1.0, 1.4), 0);
    text('MADE ON ONE ISLAND · TAIWAN', 560, 820, 30, 'BVPXBold', WHITE, 'left', fade(t, 3.2, 3.8), 1);
    text('TAIWAN STRAIT · ONLY 130 KM WIDE', 110, 900, 24, 'BVPSemi', GOLDL, 'left', fade(t, 4.6, 5.2), 2);
  }
  // image panels and stat blocks
  imgPanel('fab', 'INSIDE A TSMC FAB · TAIWAN', B1+1.0, B2-0.3, t);
  if(t >= B1 && t < B2) statBlock(B1+0.6, B2, t, Math.round(90 * eo(fade(t, B1+0.8, B1+3.2))) + '%+', GOLD, 'OF THE WORLD’S MOST ADVANCED CHIPS', 'MADE IN TAIWAN · TSMC');
  imgPanel('euv', 'ASML EUV MACHINE · NETHERLANDS', B2+1.0, B3-0.3, t);
  if(t >= B2 && t < B3) statBlock(B2+0.6, B3, t, '$' + Math.round(380 * eo(fade(t, B2+0.8, B2+3.2))) + 'M', GOLD, 'FOR ONE HIGH-NA EUV MACHINE', 'ONE MAKER ON EARTH · ASML');
  imgPanel('dc', 'AI DATA CENTER · UNITED STATES', B3+1.0, B4-0.3, t);
  if(t >= B3 && t < B4){
    const a = Math.min(fade(t, B3+0.6, B3+1.2), 1 - fade(t, B4-0.4, B4));
    text('THE DESTINATION', 110, 796, 26, 'BVPXBold', GREY, 'left', a, 2);
    text('SILICON VALLEY', 106, 886, 76, 'BVPBlack', WHITE, 'left', a, 0);
    text('WHERE WAFERS BECOME AI SERVERS', 110, 938, 24, 'BVPSemi', GREY, 'left', a, 1);
  }
  imgPanel('strait', 'TAIWAN STRAIT · SHIPPING LANE', B4+1.0, B5-0.3, t);
  if(t >= B4 && t < B5){
    const tv = (2.45 * eo(fade(t, B4+0.8, B4+3.4))).toFixed(2);
    statBlock(B4+0.6, B5, t, '$' + tv + ' TRILLION', GOLD, 'OF GOODS CROSS THIS STRAIT A YEAR · CSIS', 'MORE THAN ONE FIFTH OF WORLD SEA TRADE');
  }
  // evidence panel, fragile beat
  const ep = fade(t, B5+0.8, B5+1.6);
  if(ep > 0 && t < B6 + 0.4){
    const ea = ep * (1 - fade(t, B6-0.2, B6+0.4));
    x.save(); x.globalAlpha = ea; x.translate(0, (1-eo(ep))*50);
    glass(110, 268, 1200, 492, RED);
    text('THREE SINGLE POINTS OF FAILURE', 150, 336, 34, 'BVPBlack', WHITE, 'left', 1, 1);
    const rows = [
      ['01', 'PRODUCTION ON ONE ISLAND', 'TSMC MAKES OVER 90% OF THE WORLD’S ADVANCED CHIPS'],
      ['02', 'MACHINES FROM ONE MAKER', 'ASML IS THE ONLY SUPPLIER OF EUV LITHOGRAPHY'],
      ['03', 'EVERY ROUTE, ONE STRAIT', '$2.45 TRILLION OF GOODS A YEAR PASS THROUGH · CSIS']
    ];
    rows.forEach((r, i) => {
      const ra = fade(t, B5+1.7+i*2.6, B5+2.3+i*2.6);
      if(ra <= 0) return;
      const ry = 396 + i*118;
      x.save(); x.globalAlpha = ra * ea; x.translate((1-eo(fade(t, B5+1.7+i*2.6, B5+2.3+i*2.6)))*-46, 0);
      text(r[0], 150, ry+44, 42, 'BVPBlack', RED, 'left', 1, 0);
      text(r[1], 240, ry+16, 29, 'BVPXBold', WHITE, 'left', 1, 1);
      text(r[2], 240, ry+58, 24, 'BVPSemi', GREY, 'left', 1, 0);
      if(i < 2){ x.fillStyle = 'rgba(255,255,255,0.10)'; x.fillRect(150, ry+84, 1110, 1); }
      x.restore();
    });
    x.restore();
  }
  // closing board
  const bp = fade(t, 61.5, 62.3);
  if(bp > 0){
    x.save(); x.globalAlpha = bp; x.translate(0, (1-eo(bp))*60);
    glass(210, 660, 1500, 224, TEAL);
    text('THE PICTURE IN THREE NUMBERS', 260, 722, 24, 'BVPXBold', GREY, 'left', 1, 3);
    const cols = [
      ['90%+', 'OF ADVANCED CHIPS FROM TAIWAN', 260],
      ['$380M', 'ONE EUV MACHINE · ONE MAKER', 740],
      ['$2.45T', 'OF TRADE THROUGH ONE STRAIT', 1200]
    ];
    cols.forEach((c, i) => {
      const ca = fade(t, 62.3+i*0.9, 62.9+i*0.9);
      text(c[0], c[2], 812, 58, 'BVPBlack', GOLD, 'left', ca, 0);
      text(c[1], c[2], 854, 21, 'BVPSemi', GREY, 'left', ca, 1);
    });
    text('THE AI AGE SAILS THROUGH ONE STRAIT', 960, 646, 34, 'BVPBlack', TEAL, 'center', fade(t, 65.0, 65.8), 1);
    x.restore();
  }
  // subtitles
  subtitle('90% chip tiên tiến nhất thế giới làm trên một đảo, qua một eo biển 130 km', 0.4, B1, t);
  subtitle('Hành trình con chip AI bắt đầu tại Đài Loan, trong nhà máy TSMC', B1, B2, t);
  subtitle('Máy in chip từ Hà Lan: 380 triệu đô la một chiếc, chỉ một hãng làm được', B2, B3, t);
  subtitle('Chip tới thung lũng Silicon, thành máy chủ AI trong các trung tâm dữ liệu', B3, B4, t);
  subtitle('Eo biển này gánh 2.450 tỉ đô la hàng hoá mỗi năm (CSIS)', B4, B5, t);
  subtitle('Ba điểm mong manh: một hòn đảo, một nhà cung cấp, một eo biển', B5, B6, t);
};
window.__ready = true;
</script></body></html>"""

imgsrc = json.dumps({
    "fab": "data:image/jpeg;base64," + b64(base / "imgs/img_fab.jpg"),
    "euv": "data:image/jpeg;base64," + b64(base / "imgs/img_euv.jpg"),
    "dc": "data:image/jpeg;base64," + b64(base / "imgs/img_dc.jpg"),
    "strait": "data:image/jpeg;base64," + b64(base / "imgs/img_strait.jpg"),
})
html = (html.replace("__BLACK__", b64(fonts_dir / "BeVietnamPro-Black.ttf"))
            .replace("__XBOLD__", b64(fonts_dir / "BeVietnamPro-ExtraBold.ttf"))
            .replace("__SEMI__", b64(fonts_dir / "BeVietnamPro-SemiBold.ttf"))
            .replace("__GEO__", geo_js)
            .replace("__IMGSRC__", imgsrc))
(base / "long.html").write_text(html)
print("long.html bytes", len(html))
