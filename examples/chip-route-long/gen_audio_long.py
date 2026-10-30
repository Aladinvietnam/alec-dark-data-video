import math
import numpy as np
import soundfile as sf

SR = 48000
DUR = 68.0
N = int(DUR * SR)

def note_freq(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)

def madd(buf, at, seg):
    s0 = int(at * SR)
    if s0 >= len(buf):
        return
    n = min(len(seg), len(buf) - s0)
    buf[s0:s0 + n] += seg[:n]

# ---------- music ----------
music = np.zeros(N)
bar_s = 60.0 / 104.0 * 4.0
prog = [57, 57, 53, 55, 57, 53, 48, 55, 57, 53, 60, 55, 57, 53, 55, 55]
chord_offsets = [0, 3, 7, 12]
n_bars = int(DUR / bar_s) + 1
for j in range(n_bars):
    root = prog[j % len(prog)]
    start = j * bar_s
    n = int((bar_s + 0.45) * SR)
    tt = np.arange(n) / SR
    seg = np.zeros(n)
    for off in chord_offsets:
        f = note_freq(root + 12 + off)
        seg += np.sin(2 * np.pi * f * tt) * 0.05
        seg += np.sin(2 * np.pi * f * 2 * tt) * 0.012
    env = np.minimum(1, tt / 0.5) * np.exp(-np.maximum(0, tt - bar_s) * 4)
    madd(music, start, seg * env)
    bass_f = note_freq(root - 12)
    steps = 8
    for stp_i in range(steps):
        bs = start + stp_i * bar_s / steps
        bn = int(bar_s / steps * 0.95 * SR)
        bt = np.arange(bn) / SR
        bseg = np.sin(2 * np.pi * bass_f * bt) * np.exp(-bt * 5.5) * 0.30
        madd(music, bs, bseg)
        kn = int(0.11 * SR)
        kt = np.arange(kn) / SR
        kseg = np.sin(2 * np.pi * (120 - 500 * kt) * kt) * np.exp(-kt * 26) * 0.5
        madd(music, bs, kseg)
        if stp_i % 2 == 1:
            hn = int(0.04 * SR)
            ht = np.arange(hn) / SR
            hseg = (np.random.default_rng(stp_i * 7 + j).standard_normal(hn)) * np.exp(-ht * 130) * 0.05
            madd(music, bs, hseg)
    if j >= 2:
        sixteenth = bar_s / 16
        for k in range(16):
            f = note_freq(root + 24 + chord_offsets[k % 4] + (12 if k % 8 >= 4 else 0))
            as_ = start + k * sixteenth
            an = int(sixteenth * 0.92 * SR)
            at = np.arange(an) / SR
            aseg = np.sin(2 * np.pi * f * at) * np.exp(-at * 11) * 0.05
            madd(music, as_, aseg)

# ---------- sfx ----------
sfx = np.zeros(N)

def add(buf, at, seg):
    madd(buf, at, seg)

def boom(at, gain=0.5, dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 70 - 34 * (t / dur)
    phase = 2 * np.pi * np.cumsum(f) / SR
    add(sfx, at, np.sin(phase) * np.exp(-t * 5.0) * gain)

def riser(at, dur=0.7, gain=0.04):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 300 + 700 * (t / dur)
    phase = 2 * np.pi * np.cumsum(f) / SR
    add(sfx, at, np.sin(phase) * (t / dur) ** 2 * gain)

def whoosh(at, gain=0.16):
    n = int(0.55 * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(int(at * 10) + 3)
    noise = rng.standard_normal(n)
    # crude sweeping bandpass via amplitude-modulated harmonics of the noise envelope
    sweep = np.sin(2 * np.pi * (300 + 1900 * (t / 0.55)) * t)
    env = np.sin(np.pi * t / 0.55) ** 2
    add(sfx, at, noise * 0.35 * env * gain + sweep * 0.12 * env * gain)

def blip(at, freq=1250, gain=0.14, dur=0.09):
    n = int(dur * SR)
    t = np.arange(n) / SR
    add(sfx, at, np.sin(2 * np.pi * freq * t) * np.exp(-t * 22) * gain)

def pop(at, gain=0.20):
    n = int(0.10 * SR)
    t = np.arange(n) / SR
    add(sfx, at, np.sin(2 * np.pi * 190 * t) * np.exp(-t * 34) * gain)

def ticks(t0, t1, gain=0.05):
    at = t0
    while at < t1:
        n = int(0.02 * SR)
        t = np.arange(n) / SR
        add(sfx, at, np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 160) * gain)
        at += 0.12

# hook: counter ticks, lock beeps, impact
ticks(1.2, 3.4)
blip(1.55); blip(1.8)
riser(1.7, 0.6)
boom(2.4, 0.55, 1.0)
# camera moves
for mv in [8.8, 28.8, 36.0, 46.5, 55.8]:
    whoosh(mv)
# panel and card landings
for p in [10.4, 20.2, 30.0, 37.6]:
    pop(p)
# beat accents
boom(19.0, 0.3, 0.8)
boom(36.4, 0.35, 0.9)
ticks(37.2, 39.6, 0.04)
boom(46.9, 0.3, 0.8)
# evidence rows
for r in [48.6, 51.2, 53.8]:
    pop(r, 0.16)
# closing board
riser(60.5, 1.0, 0.05)
boom(61.6, 0.5, 1.0)
blip(65.0, 880, 0.10, 0.12)

for buf, name in [(music, "music_long.wav"), (sfx, "sfx_long.wav")]:
    peak = np.max(np.abs(buf))
    if peak > 0.95:
        buf = buf * (0.95 / peak)
    stereo = np.stack([buf, buf], axis=1)
    sf.write(name, stereo, SR)
    print(name, "peak", round(float(np.max(np.abs(buf))), 3))
print("AUDIO_LONG_DONE")
