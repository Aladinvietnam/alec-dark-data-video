from pathlib import Path

base = Path(__file__).parent
html = (base / "newstyles_part1.html").read_text()

part2 = r"""
/* ---------- 6 · PAPER COLLAGE ---------- */
function s_collage(lt){
  x.fillStyle = '#C9BB9C'; x.fillRect(0, 0, W, H);
  seed = 5;
  for(let i = 0; i < 2600; i++){
    const hx = rnd() * W, hy = rnd() * H;
    x.fillStyle = rnd() > 0.5 ? 'rgba(60,50,30,0.05)' : 'rgba(255,250,235,0.06)';
    x.beginPath(); x.arc(hx, hy, 1.6, 0, Math.PI*2); x.fill();
  }
  for(let gy = 0; gy < H; gy += 7) for(let gx = (gy % 14 ? 0 : 4); gx < W; gx += 8){
    x.fillStyle = 'rgba(40,32,18,0.045)'; x.fillRect(gx, gy, 2.4, 2.4);
  }
  text('THE RENT ATE THE CITY', 110, 190, 74, 'BVPBlack', '#1A1A1A', 'left', 1, 0);
  const uw = tw('THE RENT ATE THE CITY', 74, 'BVPBlack') * fade(lt, 0.7, 1.3);
  x.fillStyle = '#D62E1F'; x.fillRect(116, 216, uw, 10);
  function cutout(cx, cy, w, h, rot, at, drawFn, label){
    if(lt < at) return;
    const p = fade(lt, at, at + 0.45); const sc = 0.6 + 0.4 * eob(p);
    x.save(); x.translate(cx, cy); x.rotate(rot); x.scale(sc, sc); x.globalAlpha = p;
    x.shadowColor = 'rgba(59,45,18,0.38)'; x.shadowBlur = 18; x.shadowOffsetY = 9;
    x.fillStyle = '#F4EFE2'; x.fillRect(-w/2 - 9, -h/2 - 9, w + 18, h + 18);
    x.shadowColor = 'transparent'; x.shadowBlur = 0; x.shadowOffsetY = 0;
    x.save(); x.beginPath(); x.rect(-w/2, -h/2, w, h); x.clip(); drawFn(w, h); x.restore();
    x.strokeStyle = '#1A1A1A'; x.lineWidth = 2; x.strokeRect(-w/2 - 9, -h/2 - 9, w + 18, h + 18);
    x.fillStyle = 'rgba(238,231,203,0.82)'; x.fillRect(-46, -h/2 - 24, 92, 27);
    x.strokeStyle = 'rgba(120,105,70,0.35)'; x.lineWidth = 1; x.strokeRect(-46, -h/2 - 24, 92, 27);
    x.restore();
    if(label && lt > at + 0.3){
      const full = label; const n = Math.floor(full.length * fade(lt, at + 0.3, at + 1.1));
      x.save(); x.translate(cx, cy + h/2 + 44); x.rotate(rot);
      x.fillStyle = '#EDE6D2'; const lw = tw(full, 21, 'PlexMono') + 24;
      x.fillRect(-lw/2, -26, lw, 36);
      text(full.slice(0, n), 0, 0, 21, 'PlexMono', '#33302A', 'center', 1, 0);
      x.restore();
    }
  }
  cutout(430, 560, 520, 380, -0.02, 0.5, (w, h) => {
    x.fillStyle = '#8C8C8C'; x.fillRect(-w/2, -h/2, w, h);
    x.fillStyle = '#5A5A5A';
    for(let bx = -w/2 + 24; bx < w/2 - 60; bx += 92) for(let by = -h/2 + 24; by < h/2 - 60; by += 78){ x.fillRect(bx, by, 58, 52); x.fillStyle = '#A8A8A8'; x.fillRect(bx + 6, by + 6, 20, 16); x.fillStyle = '#5A5A5A'; }
    x.fillStyle = '#2A2A2A'; x.fillRect(-w/2, h/2 - 60, w, 60);
  }, 'FIG. 1 — THE BLOCK');
  cutout(1080, 520, 430, 330, 0.03, 1.5, (w, h) => {
    x.fillStyle = '#E4DCC6'; x.fillRect(-w/2, -h/2, w, h);
    x.strokeStyle = '#1A1A1A'; x.lineWidth = 4; x.beginPath();
    x.moveTo(-w/2 + 30, h/2 - 40); x.lineTo(-60, h/2 - 46); x.lineTo(30, -h/2 + 60); x.lineTo(w/2 - 40, -h/2 + 54); x.stroke();
    x.fillStyle = '#D62E1F'; x.beginPath(); x.arc(w/2 - 40, -h/2 + 54, 12, 0, Math.PI*2); x.fill();
    x.strokeStyle = '#8C8C8C'; x.lineWidth = 2;
    for(let gy = -h/2 + 40; gy < h/2; gy += 44){ x.beginPath(); x.moveTo(-w/2 + 16, gy); x.lineTo(w/2 - 16, gy); x.stroke(); }
  }, 'FIG. 2 — RENT VS WAGES');
  cutout(1560, 620, 400, 300, -0.04, 2.5, (w, h) => {
    x.fillStyle = '#3A3A3A'; x.fillRect(-w/2, -h/2, w, h);
    text('62%', 0, 30, 110, 'BVPBlack', '#F4EFE2', 'center', 1, 0);
    text('OF INCOME', 0, 84, 26, 'BVPXBold', '#D9A441', 'center', 1, 3);
  }, 'FIG. 3 — THE NUMBER');
  if(lt > 4.3){
    const p = fade(lt, 4.3, 4.55);
    x.save(); x.translate(1620, 220); x.rotate(0.16); x.globalAlpha = p; x.scale(2 - eo(p), 2 - eo(p));
    x.strokeStyle = '#D62E1F'; x.lineWidth = 5; rr(x, -150, -44, 300, 88, 8); x.stroke();
    text('VERIFIED', 0, 24, 48, 'BVPBlack', '#D62E1F', 'center', 1, 3);
    x.restore();
  }
  text('SOURCE: CITY HOUSING LEDGER · SAMPLE STORY', 110, 1010, 20, 'PlexMono', '#5A5240', 'left', 1, 1);
}
/* ---------- 7 · THRESHOLD TRACKER ---------- */
function s_threshold(lt){
  x.fillStyle = '#0B0F18'; x.fillRect(0, 0, W, H);
  text('THE NIGHT IN THREE NUMBERS', 64, 92, 40, 'BVPBlack', WHITE, 'left', 1, 1);
  const order = [0,5,2,8,1,12,4,9,3,14,6,16,10,18,7,11,13,15,17,19];
  const called = Math.floor(fade(lt, 0.3, 4.6) * 20);
  for(let i = 0; i < 20; i++){
    const cx = 90 + (i % 5) * 148, cy = 200 + Math.floor(i / 5) * 148;
    const isC = order.indexOf(i) < called;
    const col = !isC ? '#232C3E' : (i % 3 === 0 ? '#C23B4E' : '#3E6FB0');
    const tg = x.createLinearGradient(0, cy, 0, cy + 128);
    tg.addColorStop(0, mix(col, '#FFFFFF', 0.16)); tg.addColorStop(1, mix(col, '#000000', 0.14));
    x.fillStyle = tg; rr(x, cx, cy, 128, 128, 10); x.fill();
    x.strokeStyle = 'rgba(255,255,255,0.09)'; x.lineWidth = 1; rr(x, cx + 0.5, cy + 0.5, 127, 127, 10); x.stroke();
    if(isC){ x.fillStyle = 'rgba(255,255,255,0.85)'; x.beginPath(); x.arc(cx + 64, cy + 64, 10, 0, Math.PI*2); x.fill(); }
  }
  const blue = Math.round(96 + fade(lt, 0.3, 4.6) * 142 + Math.sin(lt * 2.2) * 2);
  const red = Math.round(84 + fade(lt, 0.3, 4.6) * 96);
  const bx = 880, bw = 920;
  x.fillStyle = '#232C3E'; rr(x, bx, 210, bw, 64, 10); x.fill();
  const bbG = x.createLinearGradient(0, 210, 0, 274);
  bbG.addColorStop(0, mix('#3E6FB0', '#FFFFFF', 0.22)); bbG.addColorStop(1, mix('#3E6FB0', '#000000', 0.15));
  x.fillStyle = bbG; rr(x, bx, 210, bw * (blue / 538), 64, 10); x.fill();
  const rbG = x.createLinearGradient(0, 210, 0, 274);
  rbG.addColorStop(0, mix('#C23B4E', '#FFFFFF', 0.22)); rbG.addColorStop(1, mix('#C23B4E', '#000000', 0.15));
  x.fillStyle = rbG; rr(x, bx + bw * (1 - red / 538), 210, bw * (red / 538), 64, 10); x.fill();
  const lineX = bx + bw * (270 / 538);
  x.strokeStyle = GOLD; x.lineWidth = 4; x.setLineDash([10, 8]);
  x.beginPath(); x.moveTo(lineX, 180); x.lineTo(lineX, 320); x.stroke(); x.setLineDash([]);
  text('270 TO WIN', lineX, 168, 26, 'BVPXBold', GOLD, 'center', 1, 2);
  gradText(String(blue), bx, 356, 74, 'BVPBlack', [[0, '#EAF3FF'], [0.5, '#7FA8DC'], [1, '#4A74AC']], 'left', 1, '#2A4A77');
  gradText(String(red), bx + bw, 356, 74, 'BVPBlack', [[0, '#FFE9EC'], [0.5, '#E88A98'], [1, '#B04A5E']], 'right', 1, '#772A38');
  text('ELECTORAL VOTES COUNTED', bx, 396, 20, 'BVPXBold', GREY, 'left', 1, 2);
  // needle gauge
  const gx = 1330, gy = 830;
  x.save();
  x.strokeStyle = '#39445C'; x.lineWidth = 26;
  x.beginPath(); x.arc(gx, gy, 300, Math.PI, Math.PI * 2); x.stroke();
  x.strokeStyle = '#3E6FB0'; x.beginPath(); x.arc(gx, gy, 300, Math.PI * 1.5, Math.PI * 2); x.stroke();
  x.strokeStyle = '#C23B4E'; x.beginPath(); x.arc(gx, gy, 300, Math.PI, Math.PI * 1.5); x.stroke();
  const settle = fade(lt, 0.5, 4.8);
  const jit = (1 - settle) * 0.1 * Math.sin(lt * 23) + (1 - settle) * 0.05 * Math.sin(lt * 41);
  const ang = Math.PI * (1.15 + 0.57 * settle) + jit;
  x.strokeStyle = '#F4F6FA'; x.lineWidth = 8; x.lineCap = 'round';
  x.beginPath(); x.moveTo(gx, gy); x.lineTo(gx + Math.cos(ang) * 268, gy + Math.sin(ang) * 268); x.stroke();
  x.fillStyle = 'rgba(255,255,255,0.22)'; x.beginPath(); x.arc(gx + Math.cos(ang) * 268, gy + Math.sin(ang) * 268, 13, 0, Math.PI * 2); x.fill();
  x.fillStyle = '#FFFFFF'; x.beginPath(); x.arc(gx + Math.cos(ang) * 268, gy + Math.sin(ang) * 268, 5.5, 0, Math.PI * 2); x.fill();
  x.fillStyle = '#F4F6FA'; x.beginPath(); x.arc(gx, gy, 16, 0, Math.PI*2); x.fill();
  x.restore();
  text('ESTIMATE NEEDLE · STILL MOVING', gx, gy + 132, 22, 'BVPXBold', GREY, 'center', 1, 2);
  text('COUNTED IN BATCHES, NEVER SMOOTHLY', 90, 852, 26, 'BVPXBold', '#C9CDD6', 'left', 1, 1);
  text('THE JITTER IS THE SUSPENSE', 90, 900, 26, 'BVPXBold', '#C9CDD6', 'left', 1, 1);
  srcChip(90, 962, 'SOURCE: WIRE CALLS · SAMPLE', '#E8B33C');
}
/* ---------- 8 · SLIDER EVIDENCE ---------- */
function s_slider(lt){
  x.fillStyle = '#060708'; x.fillRect(0, 0, W, H);
  ticks(38, 38, W - 76, H - 76, '#FFFFFF', 0.20);
  const blocks = [];
  seed = 23;
  for(let rI = 0; rI < 6; rI++) for(let cI = 0; cI < 11; cI++){
    blocks.push({ bx: 130 + cI * 152, by: 190 + rI * 128, bw: 118, bh: 92, gone: rnd() > 0.58, shade: 0.75 + rnd() * 0.4 });
  }
  function city(after){
    blocks.forEach(b => {
      if(after && b.gone){
        x.fillStyle = '#2A2724'; x.fillRect(b.bx, b.by + 26, b.bw, b.bh - 26);
        x.fillStyle = '#3A352F'; x.beginPath();
        x.moveTo(b.bx, b.by + 30); x.lineTo(b.bx + 30, b.by + 8); x.lineTo(b.bx + 66, b.by + 24); x.lineTo(b.bx + b.bw, b.by + 4); x.lineTo(b.bx + b.bw, b.by + 34); x.closePath(); x.fill();
        x.strokeStyle = 'rgba(255,70,60,0.85)'; x.lineWidth = 2; x.strokeRect(b.bx - 3, b.by - 3, b.bw + 6, b.bh + 6);
      } else {
        const s = Math.floor(120 * b.shade);
        const bgr = x.createLinearGradient(0, b.by, 0, b.by + b.bh);
        bgr.addColorStop(0, 'rgb(' + (s + 46) + ',' + (s + 35) + ',' + (s + 13) + ')');
        bgr.addColorStop(1, 'rgb(' + (s + 12) + ',' + (s + 4) + ',' + (s - 12) + ')');
        x.fillStyle = bgr; x.fillRect(b.bx, b.by, b.bw, b.bh);
        x.fillStyle = 'rgba(255,220,150,0.5)';
        for(let wy = 0; wy < 3; wy++) for(let wx = 0; wx < 4; wx++){ if((wx * 7 + wy * 13 + b.bx) % 3) x.fillRect(b.bx + 12 + wx * 28, b.by + 12 + wy * 26, 12, 9); }
      }
    });
  }
  city(false);
  const wipeX = 130 + fade(lt, 0.5, 4.6) * 1660;
  x.save(); x.beginPath(); x.rect(0, 0, wipeX, H); x.clip(); city(true); x.restore();
  const wg2 = x.createLinearGradient(0, 120, 0, 980);
  wg2.addColorStop(0, 'rgba(255,255,255,0.25)'); wg2.addColorStop(0.5, '#FFFFFF'); wg2.addColorStop(1, 'rgba(255,255,255,0.25)');
  x.fillStyle = wg2; x.fillRect(wipeX - 2, 120, 4, 860);
  x.fillStyle = 'rgba(14,18,26,0.88)'; x.beginPath(); x.arc(wipeX, 550, 26, 0, Math.PI*2); x.fill();
  x.strokeStyle = 'rgba(255,255,255,0.8)'; x.lineWidth = 2; x.beginPath(); x.arc(wipeX, 550, 25, 0, Math.PI*2); x.stroke();
  text('‹ ›', wipeX, 560, 26, 'BVPBlack', '#FFFFFF', 'center', 1, 0);
  text('28 OCT · AFTER', 90, 92, 28, 'BVPXBold', '#FF7A6A', 'left', 1, 2);
  text('12 OCT · BEFORE', 1830, 92, 28, 'BVPXBold', WHITE, 'right', 1, 2);
  const cnt = Math.round(224 * fade(lt, 0.5, 4.6));
  gradText('BUILDINGS DESTROYED: ' + cnt + ' OF 670', 960, 1036, 30, 'BVPXBold', WHITE_STOPS, 'center', 1, null);
  srcChip(90, 966, 'SOURCE: SATELLITE IMAGERY · SAMPLE SCENE', '#3ECF6E');
}
/* ---------- 9 · ANALOG HORROR ---------- */
function s_analog(lt){
  x.fillStyle = '#000'; x.fillRect(0, 0, W, H);
  const fx = 300, fw = 1320, fy = 90, fh = 900;
  x.save(); x.beginPath(); x.rect(fx, fy, fw, fh); x.clip();
  const glitch = (lt > 2.9 && lt < 3.06) || (lt > 4.55 && lt < 4.72);
  const jx = glitch ? (rnd() - 0.5) * 46 : 0;
  x.save(); x.translate(jx, 0);
  const g = x.createLinearGradient(0, fy, 0, fy + fh);
  g.addColorStop(0, '#2A3242'); g.addColorStop(1, '#171C28'); x.fillStyle = g; x.fillRect(fx - 60, fy, fw + 120, fh);
  text('KTV-9', fx + 70, fy + 118, 84, 'BVPBlack', '#D8DCE4', 'left', 1, 2);
  text('YOUR NEIGHBORHOOD STATION', fx + 74, fy + 158, 22, 'PlexMono', '#9AA4B5', 'left', 1, 3);
  text('EVENING SCHEDULE', fx + 70, fy + 248, 34, 'BVPXBold', '#D8DCE4', 'left', 1, 3);
  const rows = [['6:00', 'LOCAL NEWS'], ['6:30', 'WEATHER SERVICE'], ['7:00', 'FAMILY HOUR'], ['7:30', 'DO NOT WATCH', 1], ['8:00', 'LATE MOVIE'], ['9:00', 'PLEASE STAND BY', 2]];
  rows.forEach((r, i) => {
    const ry = fy + 320 + i * 74;
    const wrong = r[2] === 1 && lt > 2.2;
    const standby = r[2] === 2 && lt > 4.55;
    text(r[0], fx + 70, ry, 30, 'PlexMono', '#9AA4B5', 'left', 1, 0);
    text(standby ? 'PLEASE STAND BY' : r[1], fx + 240, ry, 32, 'BVPXBold', wrong || standby ? '#FF4A3C' : '#D8DCE4', 'left', 1, 1);
    if(glitch && wrong){ text(r[1], fx + 246, ry, 32, 'BVPXBold', 'rgba(60,200,255,0.6)', 'left', 1, 1); }
  });
  text('PM 9:47 · OCT 30 1987', fx + fw - 70, fy + fh - 44, 26, 'PlexMono', '#9AA4B5', 'right', 1, 2);
  x.restore();
  seed = Math.floor(lt * 30) * 7 + 3;
  for(let i = 0; i < 500; i++){
    x.fillStyle = 'rgba(255,255,255,' + (rnd() * 0.07) + ')';
    x.fillRect(fx + rnd() * fw, fy + rnd() * fh, 2.4, 2.4);
  }
  const bandY = fy + ((lt * 130) % (fh + 260)) - 130;
  const bg2 = x.createLinearGradient(0, bandY, 0, bandY + 110);
  bg2.addColorStop(0, 'rgba(255,255,255,0)'); bg2.addColorStop(0.5, 'rgba(255,255,255,0.10)'); bg2.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = bg2; x.fillRect(fx, bandY, fw, 110);
  for(let ly = fy; ly < fy + fh; ly += 4){ x.fillStyle = 'rgba(0,0,0,0.13)'; x.fillRect(fx, ly, fw, 1.6); }
  x.restore();
  text('RECORDED FROM A HOME TAPE · FICTION', 960, 1046, 19, 'PlexMono', '#5A6270', 'center', 1, 2);
}
/* ---------- 10 · ALERT HIJACK ---------- */
function s_alert(lt){
  x.fillStyle = '#000'; x.fillRect(0, 0, W, H);
  const hijack = lt > 3.2;
  if(hijack && lt < 3.45){ const cols = ['#C0C0C0','#C0C000','#00C0C0','#00C000','#C000C0','#C00000','#0000C0']; cols.forEach((c, i) => { x.fillStyle = c; x.fillRect(i * (W / 7), 0, W / 7, H); }); return; }
  const banG = x.createLinearGradient(0, 0, 0, 120);
  if(hijack){ banG.addColorStop(0, '#B32336'); banG.addColorStop(1, '#7E1220'); }
  else { banG.addColorStop(0, '#E7C34A'); banG.addColorStop(1, '#B98A1E'); }
  x.fillStyle = banG; x.fillRect(0, 0, W, 120);
  x.fillStyle = 'rgba(255,255,255,0.25)'; x.fillRect(0, 118, W, 2);
  text(hijack ? 'CIVIL DANGER WARNING' : 'EMERGENCY ALERT SYSTEM', 960, 80, 52, 'BVPBlack', hijack ? '#FFFFFF' : '#111111', 'center', 1, 3);
  const lines = hijack
    ? ['UPDATE — THE PREVIOUS MESSAGE', 'WAS SENT IN ERROR.', '', 'THE WARNING IS LIFTED.', 'GO OUTSIDE. LOOK AT THE SKY.']
    : ['A SEVERE EVENT HAS BEEN', 'CONFIRMED FOR THIS COUNTY.', '', 'REMAIN INDOORS.', 'DO NOT LOOK AT THE NIGHT SKY.'];
  lines.forEach((L, i) => {
    const at = hijack ? 3.5 + i * 0.16 : 0.4 + i * 0.4;
    if(lt > at){
      if(hijack && i >= 3){ x.save(); x.shadowColor = '#FF2E4D'; x.shadowBlur = 16; text(L, 960, 300 + i * 74, 44, 'BVPXBold', '#FFD9D2', 'center', fade(lt, at, at + 0.2), 1); x.restore(); }
      else text(L, 960, 300 + i * 74, 44, 'BVPXBold', i >= 3 ? '#FFD9D2' : WHITE, 'center', fade(lt, at, at + 0.2), 1);
    }
  });
  text(hijack ? 'SOURCE UNVERIFIED · FICTIONAL SCENARIO' : 'NATIONAL WEATHER SERVICE · FICTIONAL SCENARIO', 960, 720, 21, 'PlexMono', GREY, 'center', 1, 2);
  const crawl = hijack ? '+++ WARNING LIFTED +++ GO OUTSIDE +++ WARNING LIFTED +++ GO OUTSIDE +++ ' : '+++ REMAIN INDOORS +++ DO NOT LOOK AT THE NIGHT SKY +++ REMAIN INDOORS +++ ';
  x.fillStyle = '#111'; x.fillRect(0, 950, W, 74);
  x.fillStyle = 'rgba(255,255,255,0.16)'; x.fillRect(0, 950, W, 1.5);
  const off = (lt * 210) % 1400;
  text(crawl + crawl, -off, 1000, 34, 'PlexMono', hijack ? '#FF6A5A' : '#E8E8E8', 'left', 1, 1);
}
/* ---------- 11 · GHOST RADIO ---------- */
function s_ghost(lt){
  const g = x.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, '#0A1410'); g.addColorStop(0.65, '#060A08'); g.addColorStop(1, '#030504');
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  floorWash(1620, 180, 210, '#E8E4C8', 0.10);
  x.save(); x.fillStyle = '#E8E4C8'; x.shadowColor = '#E8E4C8'; x.shadowBlur = 60;
  x.beginPath(); x.arc(1620, 180, 52, 0, Math.PI*2); x.fill(); x.restore();
  x.fillStyle = '#050807'; x.fillRect(0, 800, W, 280);
  // old house
  x.fillStyle = '#070A08';
  x.fillRect(240, 520, 420, 280);
  x.beginPath(); x.moveTo(200, 520); x.lineTo(450, 380); x.lineTo(700, 520); x.closePath(); x.fill();
  x.fillRect(420, 300, 60, 90);
  const lit = lt > 4.2;
  x.fillStyle = lit ? '#FFC46A' : '#0D130E'; x.fillRect(300, 600, 74, 96);
  if(lit){ const wg = x.createRadialGradient(337, 648, 0, 337, 648, 130); wg.addColorStop(0, 'rgba(255,196,106,0.35)'); wg.addColorStop(1, 'rgba(255,196,106,0)'); x.fillStyle = wg; x.fillRect(200, 520, 280, 260); }
  x.fillStyle = '#0D130E'; x.fillRect(520, 612, 84, 188);
  // banyan tree
  x.strokeStyle = '#060806'; x.lineCap = 'round';
  x.lineWidth = 34; x.beginPath(); x.moveTo(1560, 800); x.quadraticCurveTo(1540, 560, 1470, 420); x.stroke();
  x.lineWidth = 15;
  [[1470,420,1330,330],[1470,420,1620,320],[1452,470,1300,430],[1490,460,1700,410]].forEach(b => { x.beginPath(); x.moveTo(b[0], b[1]); x.quadraticCurveTo((b[0]+b[2])/2, b[3] - 60, b[2], b[3]); x.stroke(); });
  x.lineWidth = 4;
  for(let i = 0; i < 26; i++){ const hx = 1300 + i * 17; x.beginPath(); x.moveTo(hx, 400 + (i % 5) * 14); x.lineTo(hx - 6, 560 + (i % 4) * 26); x.stroke(); }
  // fog bands drift
  for(let i = 0; i < 3; i++){
    const fy2 = 690 + i * 55; const fxo = Math.sin(lt * 0.24 + i * 2) * 90;
    const fg = x.createRadialGradient(960 + fxo, fy2, 0, 960 + fxo, fy2, 980);
    fg.addColorStop(0, 'rgba(190,210,200,0.05)'); fg.addColorStop(1, 'rgba(190,210,200,0)');
    x.fillStyle = fg; x.fillRect(0, fy2 - 130, W, 260);
  }
  // rain
  x.strokeStyle = 'rgba(180,200,210,0.16)'; x.lineWidth = 2;
  seed = 4;
  for(let i = 0; i < 90; i++){
    const rx0 = rnd() * W; const ry0 = (rnd() * H + lt * 640) % H;
    x.beginPath(); x.moveTo(rx0, ry0); x.lineTo(rx0 - 7, ry0 + 30); x.stroke();
  }
  // candle glow
  const fl = 0.85 + 0.15 * Math.sin(lt * 13) * Math.sin(lt * 7.3);
  const cg = x.createRadialGradient(120, 980, 0, 120, 980, 300 * fl);
  cg.addColorStop(0, 'rgba(255,180,90,0.20)'); cg.addColorStop(1, 'rgba(255,180,90,0)');
  x.fillStyle = cg; x.fillRect(0, 660, 640, 420);
  flameAt(120, 958, 1.1 * fl, lt, 3);
  x.fillStyle = '#D8CDB4'; rr(x, 106, 972, 28, 62, 5); x.fill();
  text('ĐÀI KỂ CHUYỆN MA · SỐ 13', 90, 110, 30, 'BVPXBold', '#B9C4B4', 'left', 1, 3);
  const story = [
    { txt: 'Đêm thứ ba, bà Tư nghe tiếng gõ cửa.', at: 0.5 },
    { txt: 'Cửa không khóa. Nhưng ngoài sân không một bóng người.', at: 2.2 },
    { txt: 'Chỉ có cửa sổ nhà đối diện… vừa sáng đèn.', at: 4.2 }
  ];
  const tb = x.createLinearGradient(300, 0, 1620, 0);
  tb.addColorStop(0, 'rgba(0,0,0,0)'); tb.addColorStop(0.5, 'rgba(0,0,0,0.42)'); tb.addColorStop(1, 'rgba(0,0,0,0)');
  x.fillStyle = tb; x.fillRect(300, 852, 1320, 196);
  story.forEach((L, i) => {
    if(lt < L.at) return;
    const n = Math.floor(L.txt.length * fade(lt, L.at, L.at + 1.1));
    text(L.txt.slice(0, n), 960, 900 + i * 56, 31, 'Georgia, serif', '#D9D4C2', 'center', 1, 0);
  });
}
/* ---------- 12 · HUNDRED CANDLES ---------- */
const CANDLE_ORDER = [7, 2, 15, 0, 20, 9, 4, 17, 11, 1, 22, 6, 13, 19, 3, 16, 8, 21, 5, 12, 23, 10, 14, 18];
function s_candles(lt){
  x.fillStyle = '#030303'; x.fillRect(0, 0, W, H);
  const dieAt = k => 0.5 + CANDLE_ORDER.indexOf(k) * 0.185;
  let litCount = 0;
  const pos = [];
  for(let rI = 0; rI < 4; rI++) for(let cI = 0; cI < 6; cI++) pos.push([300 + cI * 264, 240 + rI * 168]);
  pos.forEach((p, k) => { if(lt < dieAt(k)) litCount++; });
  const amb = 0.05 + 0.16 * (litCount / 24);
  const ag = x.createRadialGradient(960, 520, 0, 960, 520, 900);
  ag.addColorStop(0, 'rgba(255,170,80,' + amb + ')'); ag.addColorStop(1, 'rgba(255,170,80,0)');
  x.fillStyle = ag; x.fillRect(0, 0, W, H);
  pos.forEach((p, k) => {
    const dead = lt >= dieAt(k);
    if(lt < dieAt(k)) floorWash(p[0], p[1] + 80, 58, '#FFAA50', 0.12);
    const cg2 = x.createLinearGradient(0, p[1], 0, p[1] + 74);
    cg2.addColorStop(0, '#E7DFC8'); cg2.addColorStop(1, '#A99B78');
    x.fillStyle = cg2; rr(x, p[0] - 17, p[1], 34, 74, 6); x.fill();
    x.fillStyle = '#A89A7C'; x.fillRect(p[0] - 17, p[1], 34, 10);
    if(!dead){
      const hg = x.createRadialGradient(p[0], p[1] - 18, 0, p[0], p[1] - 18, 64);
      hg.addColorStop(0, 'rgba(255,170,80,0.16)'); hg.addColorStop(1, 'rgba(255,170,80,0)');
      x.fillStyle = hg; x.fillRect(p[0] - 64, p[1] - 82, 128, 128);
      flameAt(p[0], p[1] - 16, 1.05, lt, k * 1.7);
    }
    else {
      const sage = lt - dieAt(k);
      if(sage < 1.6){
        x.save(); x.strokeStyle = 'rgba(190,190,200,' + (0.4 * (1 - sage / 1.6)) + ')'; x.lineWidth = 3.4; x.lineCap = 'round';
        x.beginPath();
        for(let s2 = 0; s2 <= 8; s2++){ const wy = p[1] - 26 - s2 * 9 * (0.4 + sage); const wx = p[0] + Math.sin(s2 * 1.2 + sage * 3) * (3 + sage * 7); s2 ? x.lineTo(wx, wy) : x.moveTo(wx, wy); }
        x.stroke(); x.restore();
      }
    }
  });
  gradText('MỖI NGỌN NẾN, MỘT CÁI TÊN', 960, 104, 34, 'BVPXBold', [[0, '#FFF3D6'], [0.55, '#D9CFB8'], [1, '#978A6C']], 'center', 1, null);
  text('CÒN LẠI ' + litCount + ' / 24 NGỌN', 960, 1006, 30, 'BVPXBold', litCount <= 6 ? '#FF8A7A' : '#B9AE94', 'center', 1, 3);
}
/* ---------- REGISTRY + REEL ---------- */
const SEGS = [
  { fn: s_flood, name: 'BORDER FLOOD', genre: 'STORYTELLING · MAP HISTORY' },
  { fn: s_chat, name: 'CHAT THREAD', genre: 'STORYTELLING' },
  { fn: s_case, name: 'CASE FILE', genre: 'STORYTELLING · TRUE CRIME' },
  { fn: s_race, name: 'BAR RACE', genre: 'ECONOMICS' },
  { fn: s_river, name: 'MONEY RIVER', genre: 'ECONOMICS' },
  { fn: s_risefall, name: 'RISE AND FALL', genre: 'ECONOMICS · DOCUMENTARY' },
  { fn: s_collage, name: 'PAPER COLLAGE', genre: 'NEWS · VOX STYLE' },
  { fn: s_threshold, name: 'THRESHOLD TRACKER', genre: 'NEWS · ELECTIONS' },
  { fn: s_slider, name: 'SLIDER EVIDENCE', genre: 'NEWS · INVESTIGATION' },
  { fn: s_analog, name: 'ANALOG HORROR', genre: 'HORROR' },
  { fn: s_alert, name: 'ALERT HIJACK', genre: 'HORROR · EAS' },
  { fn: s_ghost, name: 'GHOST RADIO', genre: 'HORROR · TRUYỆN MA' },
  { fn: s_candles, name: 'HUNDRED CANDLES', genre: 'HORROR · ORIGINAL FUSION' }
];
const SEGD = 5.5;
window.renderScene = function(i, lt){
  x.clearRect(0, 0, W, H);
  SEGS[i].fn(lt);
  finishFrame(i, lt);
};
window.render = function(t){
  const i = Math.min(SEGS.length - 1, Math.floor(t / SEGD));
  const lt = t - i * SEGD;
  x.clearRect(0, 0, W, H);
  SEGS[i].fn(lt);
  finishFrame(i, lt);
  const chip = 'STYLE ' + String(i + 1).padStart(2, '0') + ' · ' + SEGS[i].name;
  const cw = tw(chip, 21, 'BVPXBold') + 58;
  const chipY = i === 10 ? 856 : (i === 0 || i === 3) ? 44 : 972;
  glassPanel(1872 - cw, chipY, cw, 46, 23, 'rgba(10,13,22,0.82)');
  x.fillStyle = GOLD; x.beginPath(); x.arc(1872 - cw + 22, chipY + 23, 5, 0, Math.PI * 2); x.fill();
  x.fillStyle = 'rgba(232,179,60,0.28)'; x.beginPath(); x.arc(1872 - cw + 22, chipY + 23, 11, 0, Math.PI * 2); x.fill();
  text(chip, 1872 - cw + 36, chipY + 30, 21, 'BVPXBold', GOLD, 'left', 1, 1);
  text(SEGS[i].genre, 48, 1046, 19, 'BVPXBold', 'rgba(230,235,245,0.55)', 'left', 1, 2);
  const fin = fade(lt, 0, 0.3), fout = fade(lt, SEGD - 0.3, SEGD);
  const black = Math.max(1 - fin, fout);
  if(black > 0){ x.fillStyle = 'rgba(0,0,0,' + black + ')'; x.fillRect(0, 0, W, H); }
};
window.__ready = true;
</script>"""

html = html.replace("</script>", part2)
(base / "newstyles.html").write_text(html)
print("newstyles.html bytes", len(html))
