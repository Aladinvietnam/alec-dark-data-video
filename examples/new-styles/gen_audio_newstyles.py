import numpy as np
import soundfile as sf

SR = 48000
DUR = 71.5
N = int(DUR * SR)
bed = np.zeros(N)
sfx = np.zeros(N)

def madd(buf, at, seg):
    s0 = int(at * SR)
    if s0 >= len(buf):
        return
    n = min(len(seg), len(buf) - s0)
    buf[s0:s0 + n] += seg[:n]

def freq(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)

beat = 60.0 / 100.0
bar = beat * 4
roots = [45, 43, 41, 48, 45, 43, 50, 47]
bar_i = 0
start = 0.0
while start < DUR:
    root = roots[bar_i % len(roots)]
    n = int(min(bar + 0.3, DUR - start) * SR)
    tt = np.arange(n) / SR
    seg = np.zeros(n)
    for off in [0, 3, 7, 12]:
        seg += np.sin(2 * np.pi * freq(root + 12 + off) * tt) * 0.026
    env = np.minimum(1, tt / 0.5) * np.exp(-np.maximum(0, tt - bar) * 2.5)
    madd(bed, start, seg * env)
    for s2 in range(8):
        bs = start + s2 * beat / 2
        bn = int(0.16 * SR)
        bt = np.arange(bn) / SR
        madd(bed, bs, np.sin(2 * np.pi * freq(root - 12) * bt) * np.exp(-bt * 9) * 0.22)
        if s2 % 2 == 0:
            kn = int(0.08 * SR)
            kt = np.arange(kn) / SR
            madd(bed, bs, np.sin(2 * np.pi * (130 - 480 * kt) * kt) * np.exp(-kt * 32) * 0.3)
    start += bar
    bar_i += 1

def pop(at, gain=0.2):
    n = int(0.1 * SR)
    t = np.arange(n) / SR
    madd(sfx, at, np.sin(2 * np.pi * 190 * t) * np.exp(-t * 28) * gain)

def boom(at, gain=0.4, dur=0.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 72 - 34 * (t / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    madd(sfx, at, np.sin(ph) * np.exp(-t * 5) * gain)

def tick(at, gain=0.05):
    n = int(0.025 * SR)
    t = np.arange(n) / SR
    madd(sfx, at, np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 130) * gain)

def glitch(at, dur=0.22, gain=0.16):
    n = int(dur * SR)
    rng = np.random.default_rng(int(at * 10))
    seg = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 4) * gain
    seg[::37] *= 2.2
    madd(sfx, at, seg)

def beep(at, f0=880, dur=0.35, gain=0.045):
    n = int(dur * SR)
    t = np.arange(n) / SR
    madd(sfx, at, np.sin(2 * np.pi * f0 * t) * np.minimum(1, t / 0.02) * gain)

for s2 in range(13):
    pop(s2 * 5.5 + 0.06, 0.16)
# chat pops
for dt in [0.3, 1.0, 1.8, 3.0, 3.7, 4.5]:
    pop(5.5 + dt, 0.12)
# collage typewriter ticks
at = 33.0 + 1.8
while at < 33.0 + 3.2:
    tick(at, 0.04)
    at += 0.09
at = 33.0 + 2.8
while at < 33.0 + 4.0:
    tick(at, 0.04)
    at += 0.09
# rise and fall cliff
boom(27.5 + 3.55, 0.42, 0.9)
# analog glitch bursts
glitch(49.5 + 2.9)
glitch(49.5 + 4.55)
# alert beeps
beep(55.0 + 0.15, 880, 0.4)
beep(55.0 + 3.25, 660, 0.4)
# ghost radio low swell
n = int(5.5 * SR)
tt = np.arange(n) / SR
madd(bed, 60.5, np.sin(2 * np.pi * 55 * tt) * 0.05 * np.sin(np.pi * tt / 5.5))

for buf, name in [(bed, "bed_ns.wav"), (sfx, "sfx_ns.wav")]:
    peak = np.max(np.abs(buf))
    if peak > 0.95:
        buf = buf * (0.95 / peak)
    sf.write(name, np.stack([buf, buf], axis=1), SR)
    print(name, "peak", round(float(np.max(np.abs(buf))), 3))
print("NS_AUDIO_DONE")
