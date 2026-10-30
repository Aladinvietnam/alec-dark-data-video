import base64
from pathlib import Path

base = Path(__file__).parent
import os
fonts_dir = Path(os.environ.get("ALEC_FONT_DIR", Path(__file__).parent / "fonts"))

def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()

black = b64(fonts_dir / "BeVietnamPro-Black.ttf")
xbold = b64(fonts_dir / "BeVietnamPro-ExtraBold.ttf")
semi = b64(fonts_dir / "BeVietnamPro-SemiBold.ttf")

html = r"""<!doctype html>
<html><head><meta charset="utf-8">
<style>
@font-face{font-family:BVPBlack;src:url(data:font/ttf;base64,__BLACK__) format('truetype');}
@font-face{font-family:BVPXBold;src:url(data:font/ttf;base64,__XBOLD__) format('truetype');}
@font-face{font-family:BVPSemi;src:url(data:font/ttf;base64,__SEMI__) format('truetype');}
html,body{margin:0;padding:0;background:#050507;overflow:hidden;}
canvas{display:block;}
</style></head>
<body>
<canvas id="c" width="1920" height="1080"></canvas>
<script>
const cv = document.getElementById('c');
const x = cv.getContext('2d');
const W = 1920, H = 1080, DUR = 35.4;
const GOLD = '#FFC21A', GOLDL = '#FFDF4D', RED = '#FF4A3D', REDL = '#FF8A70', TEAL = '#2BD9A9', WHITE = '#F7F5EF', GREY = '#A7B0BA', CARD = '#101014';
const B0 = 4.6, C0 = 9.1, E0 = 15.9, F0 = 27.2, BADGE = 14.7;

function clamp(v,a,b){ return Math.max(a, Math.min(b, v)); }
function easeOut(p){ return 1 - Math.pow(1-p, 3); }
function easeInOut(p){ return p<0.5 ? 2*p*p : 1-Math.pow(-2*p+2,2)/2; }
function easeOutBack(p){ const c = 1.35; return 1 + (c+1)*Math.pow(p-1,3) + c*Math.pow(p-1,2); }
function fade(t,a,b){ return clamp((t-a)/(b-a),0,1); }
function slam(t,a,dur){ const p = clamp((t-a)/dur,0,1); return 1 + (1-easeOut(p))*0.55; }
function rr(ctx,px,py,w,h,r){ ctx.beginPath(); ctx.moveTo(px+r,py); ctx.arcTo(px+w,py,px+w,py+h,r); ctx.arcTo(px+w,py+h,px,py+h,r); ctx.arcTo(px,py+h,px,py,r); ctx.arcTo(px,py,px+w,py,r); ctx.closePath(); }
function text(str,px,py,size,font,color,align,alpha,spacing){
  x.save(); x.globalAlpha = alpha==null?1:alpha; x.fillStyle = color;
  x.font = size + 'px ' + font; x.textAlign = align||'left'; x.textBaseline = 'alphabetic';
  if(spacing){ try{ x.letterSpacing = spacing + 'px'; }catch(e){} }
  x.fillText(str,px,py); x.restore();
}
function tw(str,size,font){ x.save(); x.font = size + 'px ' + font; const w = x.measureText(str).width; x.restore(); return w; }

const BASE = 792, MAXH = 372;
function hFor(v){ return MAXH * (v/5.9); }
function fitSize(str, maxW, size, font){ let s = size; while(s > 16 && tw(str, s, font) > maxW){ s -= 1; } return s; }
const STARS = [];
{ let seed = 42; const rnd = ()=>{ seed = (seed*1103515245 + 12345) % 2147483648; return seed/2147483648; };
  for(let i=0;i<110;i++){ STARS.push({ sx: rnd()*1920, sy: rnd()*1080, sr: rnd()*1.7+0.5, sa: rnd()*0.17+0.06 }); } }

function subtitle(str, a, b, t){
  const al = Math.min(fade(t,a,a+0.35), 1 - fade(t,b-0.3,b));
  if(al <= 0) return;
  const size = fitSize(str, 1480, 30, 'BVPSemi');
  const w = tw(str,size,'BVPSemi') + 76;
  x.save(); x.globalAlpha = al*0.94; x.fillStyle = 'rgba(13,17,38,0.88)';
  rr(x, 960-w/2, 920, w, 58, 29); x.fill();
  x.strokeStyle = 'rgba(255,255,255,0.20)'; x.lineWidth = 1; rr(x, 960-w/2, 920, w, 58, 29); x.stroke();
  x.restore();
  text(str, 960, 958, size,'BVPSemi',WHITE,'center',al,0);
}

function render(t){
  x.clearRect(0,0,W,H);
  // deep navy base with drifting aurora blobs and fine stars
  const g = x.createLinearGradient(0,0,1920,1080);
  g.addColorStop(0,'#182259'); g.addColorStop(0.5,'#10173F'); g.addColorStop(1,'#080C22');
  x.fillStyle = g; x.fillRect(0,0,W,H);
  function blob(cx,cy,r,color,alpha){
    const bg = x.createRadialGradient(cx,cy,0,cx,cy,r);
    bg.addColorStop(0,color.replace('A', String(alpha))); bg.addColorStop(1,color.replace('A','0'));
    x.fillStyle = bg; x.fillRect(cx-r,cy-r,r*2,r*2);
  }
  blob(430 + 60*Math.sin(t*0.11), 190 + 40*Math.cos(t*0.09), 680, 'rgba(139,63,255,A)', 0.34);
  blob(1500 + 70*Math.cos(t*0.08), 130 + 34*Math.sin(t*0.10), 560, 'rgba(46,116,255,A)', 0.28);
  blob(1640 + 56*Math.sin(t*0.07+2), 900 + 44*Math.cos(t*0.08+1), 740, 'rgba(16,212,178,A)', 0.24);
  blob(960 + 80*Math.sin(t*0.06+4), 1010, 620, 'rgba(224,64,251,A)', 0.15);
  x.save(); x.fillStyle = '#FFFFFF';
  STARS.forEach(s=>{ x.globalAlpha = s.sa; x.beginPath(); x.arc(s.sx, s.sy, s.sr, 0, Math.PI*2); x.fill(); });
  x.restore();
  const vg = x.createRadialGradient(960,500,420, 960,500,1180);
  vg.addColorStop(0,'rgba(0,0,0,0)'); vg.addColorStop(1,'rgba(0,0,0,0.42)');
  x.fillStyle = vg; x.fillRect(0,0,W,H);

  // slow camera push in across the whole clip
  const zoom = 1 + 0.028*easeInOut(clamp(t/DUR,0,1));
  x.save(); x.translate(960,540); x.scale(zoom,zoom); x.translate(-960,-540);

  x.save(); x.strokeStyle = 'rgba(255,255,255,0.05)'; x.lineWidth = 1;
  for(let gy=160; gy<H; gy+=92){ x.beginPath(); x.moveTo(0,gy); x.lineTo(W,gy); x.stroke(); }
  x.restore();

  // red glow behind the Binance bar, grows with phase C
  const p2raw = fade(t, C0+0.5, BADGE);
  if(p2raw > 0){
    const rg = x.createRadialGradient(1300,600,40, 1300,600,560);
    rg.addColorStop(0,'rgba(255,60,40,' + (0.20*p2raw) + ')'); rg.addColorStop(1,'rgba(255,60,40,0)');
    x.fillStyle = rg; x.fillRect(700,60,1220,980);
  }

  // header
  const hs = slam(t,0,0.22);
  x.save(); x.translate(120,118); x.scale(hs,hs); x.translate(-120,-118);
  text('BINANCE HACKED',120,118,66,'BVPBlack',WHITE,'left',1,1);
  x.restore();
  text('THE BIGGEST CRYPTO HEIST EVER',122,168,33,'BVPXBold',GOLD,'left',fade(t,0.35,0.9),3);
  x.save(); x.globalAlpha = fade(t,0.2,0.6);
  const chipW = tw('OCT 29 · 2026',30,'BVPXBold') + 60;
  x.fillStyle = '#D61F14'; rr(x, W-120-chipW, 62, chipW, 62, 31); x.fill();
  text('OCT 29 · 2026', W-120-chipW/2, 104, 30,'BVPXBold',WHITE,'center',1,1);
  x.restore();
  text('SOURCES · COINDESK / CHAINALYSIS / BINANCE', W-120, 168, 20,'BVPSemi',GREY,'right',fade(t,0.6,1.2),1);
  // refined hairline under the header zone, gold fading to transparent
  x.save(); x.globalAlpha = 0.5*fade(t,0.5,1.1);
  const hl = x.createLinearGradient(120,0,1800,0);
  hl.addColorStop(0,'rgba(255,194,26,0.55)'); hl.addColorStop(0.45,'rgba(255,255,255,0.14)'); hl.addColorStop(1,'rgba(255,255,255,0)');
  x.fillStyle = hl; x.fillRect(120, 192, 1680, 1.5); x.restore();

  // phase A alert symbol with expanding rings, fades out as phase B starts
  const alertA = 1 - fade(t, B0-0.5, B0);
  if(alertA > 0){
    const cx = 960, cy = 305;
    for(let k=0;k<2;k++){
      const ph = ((t*0.55 + k*0.5) % 1);
      x.save(); x.globalAlpha = alertA * 0.5*(1-ph);
      x.strokeStyle = RED; x.lineWidth = 5;
      x.beginPath(); x.arc(cx,cy, 74 + ph*86, 0, Math.PI*2); x.stroke(); x.restore();
    }
    const pulse = 1 + 0.05*Math.sin(t*6);
    x.save(); x.translate(cx,cy); x.scale(pulse,pulse);
    x.strokeStyle = RED; x.lineWidth = 11;
    x.beginPath(); x.arc(0,0,70,0,Math.PI*2); x.stroke();
    text('!', 0, 34, 96,'BVPBlack',RED,'center',alertA,0);
    x.restore();
    // pulsing red border during phase A
    x.save(); x.globalAlpha = alertA * (0.22 + 0.16*Math.sin(t*5));
    x.strokeStyle = RED; x.lineWidth = 7; x.strokeRect(4,4,W-8,H-8); x.restore();
  }

  // hero number
  let hero = null, heroLabel = '';
  if(t >= B0-0.2 && t < C0){
    const p = easeOut(fade(t, B0+0.4, C0-0.6));
    hero = 1.5*p; heroLabel = 'THE OLD RECORD · BYBIT 2025';
  } else if(t >= C0){
    const p = easeOut(fade(t, C0+0.5, BADGE));
    hero = 1.5 + (5.9-1.5)*p; heroLabel = 'ESTIMATED STOLEN · CHAINALYSIS';
  }
  if(hero !== null){
    text(heroLabel, 960, 238, 27,'BVPSemi',GREY,'center',1,4);
    let bump = 1;
    if(t >= BADGE && t < BADGE+0.55) bump = 1 + 0.07*(1-(t-BADGE)/0.55);
    x.save(); x.translate(960,356); x.scale(bump,bump); x.translate(-960,-356);
    text('$' + hero.toFixed(1) + ' BILLION', 960, 356, 138,'BVPBlack',GOLD,'center',1,0);
    x.restore();
  }

  // gridlines
  x.save(); x.strokeStyle='rgba(255,255,255,0.14)'; x.setLineDash([7,9]); x.lineWidth=1.5;
  [1.5,5.9].forEach(v=>{ const gy = BASE - hFor(v); x.beginPath(); x.moveTo(180,gy); x.lineTo(1740,gy); x.stroke(); });
  x.restore();
  text('$1.5B',162,BASE-hFor(1.5)+8,22,'BVPSemi',GREY,'right',fade(t,B0,B0+0.6));
  text('$5.9B',162,BASE-hFor(5.9)+8,22,'BVPSemi',GREY,'right',fade(t,C0,C0+0.8));

  // bars with overshoot growth and glow
  const p1 = easeOutBack(fade(t, B0+0.4, C0-0.6));
  const p2 = easeOutBack(fade(t, C0+0.5, BADGE));
  const gh = hFor(1.5)*Math.max(0,p1);
  if(gh > 2){
    const gg = x.createLinearGradient(0,BASE-gh,0,BASE); gg.addColorStop(0,GOLDL); gg.addColorStop(1,'#FF9E00');
    x.save(); x.shadowColor = 'rgba(255,194,26,0.65)'; x.shadowBlur = 50;
    x.fillStyle = gg; x.fillRect(470, BASE-gh, 300, gh); x.restore();
    if(p1 > 0.55) text('$1.5B', 620, BASE-gh+52, 40,'BVPBlack','#231600','center',fade(t,C0-1.6,C0-0.9),0);
  }
  const rh = hFor(5.9)*Math.max(0,p2);
  if(rh > 2){
    const rg2 = x.createLinearGradient(0,BASE-rh,0,BASE); rg2.addColorStop(0,REDL); rg2.addColorStop(1,'#E8110C');
    x.save(); x.shadowColor = 'rgba(255,60,40,0.7)'; x.shadowBlur = 62;
    x.fillStyle = rg2; x.fillRect(1150, BASE-rh, 300, rh); x.restore();
    if(p2 > 0.55) text('$5.9B', 1300, BASE-rh+56, 44,'BVPBlack',WHITE,'center',fade(t,BADGE-1.2,BADGE-0.5),0);
  }
  x.fillStyle = 'rgba(247,245,239,0.55)'; x.fillRect(180, BASE, 1560, 3);

  // bar captions
  text('BYBIT',620,BASE+58,42,'BVPXBold',WHITE,'center',fade(t,B0+0.8,B0+1.4),1);
  text('2025 · PREVIOUS RECORD',620,BASE+94,24,'BVPSemi',GREY,'center',fade(t,B0+1.0,B0+1.6),2);
  text('BINANCE',1300,BASE+58,42,'BVPXBold',WHITE,'center',fade(t,C0+0.9,C0+1.5),1);
  text('2026 · WORLD’S LARGEST EXCHANGE',1300,BASE+94,24,'BVPSemi',RED,'center',fade(t,C0+1.1,C0+1.7),2);

  // badge slam with flash and ring
  if(t >= BADGE){
    const s = slam(t,BADGE,0.2);
    x.save(); x.translate(960,470); x.rotate(-0.07); x.scale(s,s);
    const bw = tw('4X BIGGER',56,'BVPBlack') + 64;
    x.fillStyle = GOLD; rr(x,-bw/2,-46,bw,92,12); x.fill();
    text('4X BIGGER',0,20,56,'BVPBlack','#0A0A0A','center',1,1);
    x.restore();
    const rp = (t-BADGE)/0.9;
    if(rp < 1){
      x.save(); x.globalAlpha = 0.75*(1-rp); x.strokeStyle = GOLD; x.lineWidth = 6;
      x.beginPath(); x.arc(960,470, 60 + rp*330, 0, Math.PI*2); x.stroke(); x.restore();
    }
    if(t < BADGE+0.3){
      x.save(); x.globalAlpha = 0.26*(1-(t-BADGE)/0.3); x.fillStyle = '#FFFFFF'; x.fillRect(0,0,W,H); x.restore();
    }
  }

  // investigation panel, cause analysis in evidence board style
  const panelA = Math.min(fade(t, E0+0.15, E0+0.85), 1 - fade(t, F0-0.45, F0));
  if(panelA > 0){
    x.save(); x.globalAlpha = 0.52*panelA; x.fillStyle = '#04061A';
    x.fillRect(150, 392, 1620, 512); x.restore();
    const pdy = (1 - easeOut(fade(t, E0+0.15, E0+0.85))) * 42;
    x.save(); x.globalAlpha = panelA; x.translate(0, pdy);
    x.shadowColor = 'rgba(0,0,0,0.5)'; x.shadowBlur = 34; x.shadowOffsetY = 12;
    x.fillStyle = 'rgba(11,16,40,0.94)'; rr(x, 330, 408, 1260, 396, 18); x.fill();
    x.shadowColor = 'transparent'; x.shadowBlur = 0; x.shadowOffsetY = 0;
    x.strokeStyle = 'rgba(255,255,255,0.20)'; x.lineWidth = 1; rr(x, 330, 408, 1260, 396, 18); x.stroke();
    text('HOW DID IT HAPPEN?', 368, 480, 37,'BVPXBold',WHITE,'left',1,1);
    const invW = tw('INVESTIGATION',22,'BVPXBold') + 44;
    x.fillStyle = '#D61F14'; rr(x, 1590-invW, 442, invW, 40, 20); x.fill();
    text('INVESTIGATION', 1590-invW/2, 470, 22,'BVPXBold',WHITE,'center',1,1);
    text('EARLY FINDINGS · SUSPECTED, NOT CONFIRMED', 368, 516, 20,'BVPSemi',GREY,'left',1,2);
    const rows = [
      ['SIGNING PROCESS MANIPULATED?', 'BLOCKAID SUSPECTS SIGNATURE ABUSE, NOT A KEY THEFT', E0+0.8],
      ['WALLET PERMISSION ABUSED?', 'ARKHAM POINTS TO EIP-7702 DELEGATION RISK', E0+4.0],
      ['MONEY PUSHED THROUGH DEFI', 'UNISWAP SWAPS TRACED · $44M BORROWED VIA AAVE', E0+7.2]
    ];
    x.save(); x.strokeStyle = 'rgba(255,194,26,0.5)'; x.lineWidth = 3;
    x.beginPath(); x.moveTo(404, 566); x.lineTo(404, 752); x.stroke(); x.restore();
    rows.forEach((row, i)=>{
      const ry = 536 + i*86;
      const rp = fade(t, row[2], row[2]+0.55);
      if(rp <= 0) return;
      const rdx = (1 - easeOutBack(rp)) * 130;
      x.save(); x.globalAlpha = panelA * clamp(rp*1.4,0,1); x.translate(rdx, 0);
      x.fillStyle = 'rgba(7,10,26,0.9)'; x.beginPath(); x.arc(404, ry+30, 22, 0, Math.PI*2); x.fill();
      x.strokeStyle = GOLD; x.lineWidth = 2.5; x.beginPath(); x.arc(404, ry+30, 22, 0, Math.PI*2); x.stroke();
      text('0' + (i+1), 404, ry+38, 20,'BVPXBold',GOLD,'center',1,0);
      const ts = fitSize(row[0], 1080, 29, 'BVPXBold');
      text(row[0], 452, ry+36, ts,'BVPXBold',WHITE,'left',1,1);
      const ss = fitSize(row[1], 1080, 21, 'BVPSemi');
      text(row[1], 452, ry+66, ss,'BVPSemi',GREY,'left',1,1);
      x.restore();
    });
    x.restore();
  }

  // subtitles for segments A to C
  subtitle('Binance vừa bị hack — vụ trộm tiền ảo lớn nhất lịch sử', 0.35, B0, t);
  subtitle('Kỷ lục cũ: Bybit 2025 — 1,5 tỉ đô la', B0, C0, t);
  subtitle('Chainalysis ước tính 5,9 tỉ đô la — gấp 4 lần kỷ lục cũ', C0, E0, t);
  subtitle('Điều tra: nghi can thiệp chữ ký giao dịch — tiền bị đẩy qua DeFi', E0, F0, t);

  // phase D verdict, measured layout so the three items can never touch
  const va = fade(t, F0+0.3, F0+1.1);
  if(va > 0){
    const dy = (1-easeOut(va))*26;
    const items = [ ['BTC −5% · BELOW $77K', RED], ['WITHDRAWALS PAUSED', WHITE], ['BINANCE · LOSSES COVERED', TEAL] ];
    const VS = 30, GAP = 76;
    const widths = items.map(it => tw(it[0], VS, 'BVPXBold'));
    const totalW = widths.reduce((a,b)=>a+b,0) + GAP*(items.length-1);
    let vx = 960 - totalW/2;
    x.save(); x.globalAlpha = va;
    items.forEach((it,i)=>{ text(it[0], vx, 950+dy, VS,'BVPXBold',it[1],'left',1,1); vx += widths[i] + GAP; });
    x.restore();
  }

  // phase D cards, slide up with teal frozen accents
  function card(cx,cw,start,title,sub){
    const p = easeOutBack(fade(t,start,start+0.65));
    if(fade(t,start,start+0.65) <= 0) return;
    const dy = (1-p)*90;
    x.save(); x.globalAlpha = clamp(fade(t,start,start+0.4),0,1);
    x.translate(0,dy);
    x.shadowColor = 'rgba(0,0,0,0.45)'; x.shadowBlur = 26; x.shadowOffsetY = 10;
    x.fillStyle = 'rgba(15,20,42,0.86)'; rr(x,cx,968,cw,92,16); x.fill();
    x.shadowColor = 'transparent'; x.shadowBlur = 0; x.shadowOffsetY = 0;
    x.strokeStyle = 'rgba(255,255,255,0.15)'; x.lineWidth = 1; rr(x,cx,968,cw,92,16); x.stroke();
    x.fillStyle = TEAL; rr(x,cx+22,968+14,5,64,2.5); x.fill();
    const ts = fitSize(title, cw-120, 33, 'BVPXBold');
    text(title, cx+48, 1006, ts,'BVPXBold',TEAL,'left',1,0);
    text(sub, cx+48, 1040, 22,'BVPSemi',GREY,'left',1,2);
    x.restore();
  }
  card(180, 820, F0+0.9, '$3.0 BILLION FROZEN', 'BINANCE VERIFIED TOTAL');
  card(1040, 700, F0+1.9, 'TETHER $1.57B · CIRCLE $0.8B+', 'STABLECOINS FROZEN BY ISSUERS');

  x.restore(); // camera zoom
}
window.render = render;
render(0);
window.__ready = true;
</script>
</body></html>
"""

html = html.replace("__BLACK__", black).replace("__XBOLD__", xbold).replace("__SEMI__", semi)
(base / "scene.html").write_text(html)
print("scene.html bytes", len(html))
