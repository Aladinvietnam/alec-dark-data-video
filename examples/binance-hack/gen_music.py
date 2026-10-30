import numpy as np
import soundfile as sf
from pathlib import Path

SR = 48000
DUR = 35.4
N = int(SR * DUR)
out = np.zeros(N)
BPM = 104.0
BEAT = 60.0 / BPM
BAR = BEAT * 4

def freq(midi):
    return 440.0 * 2 ** ((midi - 69) / 12.0)

def add(start, wave):
    i = int(start * SR)
    j = min(N, i + len(wave))
    if j > i:
        out[i:j] += wave[: j - i]

def env_adsr(n, a, d, s_level, r):
    t = np.arange(n) / SR
    env = np.ones(n) * s_level
    env = np.where(t < a, t / a, env)
    dec = (t >= a) & (t < a + d)
    env = np.where(dec, 1 - (1 - s_level) * (t - a) / d, env)
    rel = t > (n / SR - r)
    env = np.where(rel, env * np.clip((n / SR - t) / r, 0, 1), env)
    return env

def pad_chord(start, midis, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    wave = np.zeros(n)
    for m in midis:
        f = freq(m)
        wave += np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2 * t)
    wave /= len(midis)
    add(start, wave * env_adsr(n, 0.4, 0.6, 0.55, 0.5) * 0.16)

def bass(start, midi, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq(midi)
    wave = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2 * t)
    env = np.exp(-t * 3.2)
    add(start, wave * env * 0.34)

def pluck(start, midi, gain=0.15):
    dur = 0.34
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq(midi)
    wave = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2 * t) + 0.15 * np.sin(2 * np.pi * f * 3 * t)
    add(start, wave * np.exp(-t * 11) * gain)

def kick(start):
    dur = 0.26
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 115 - 70 * (t / dur)
    phase = 2 * np.pi * np.cumsum(f) / SR
    add(start, np.sin(phase) * np.exp(-t * 13) * 0.5)

def hat(start, gain=0.045):
    dur = 0.05
    n = int(dur * SR)
    rng = np.random.default_rng(int(start * 1000) + 7)
    noise = rng.standard_normal(n)
    hp = np.diff(noise, prepend=0)
    t = np.arange(n) / SR
    add(start, hp * np.exp(-t * 90) * gain)

# Chord progression per bar: Am, Am, F, G, Am, F, C, G, Am, F
progression = [
    (45, [57, 60, 64]),
    (45, [57, 60, 64]),
    (41, [53, 57, 60]),
    (43, [55, 59, 62]),
    (45, [57, 60, 64]),
    (41, [53, 57, 60]),
    (48, [55, 60, 64]),
    (43, [55, 59, 62]),
    (45, [57, 60, 64]),
    (41, [53, 57, 60]),
    (45, [57, 60, 64]),
    (41, [53, 57, 60]),
    (48, [55, 60, 64]),
    (43, [55, 59, 62]),
    (45, [57, 60, 64]),
    (41, [53, 57, 60]),
]
arp_pattern = [0, 1, 2, 1, 0, 2, 1, 2]

for bar_i, (root, chord) in enumerate(progression):
    bs = bar_i * BAR
    if bs >= DUR:
        break
    pad_chord(bs, chord, BAR + 0.3)
    for b in range(4):
        kick(bs + b * BEAT)
        bass(bs + b * BEAT, root, BEAT * 0.95)
        hat(bs + b * BEAT + BEAT / 2)
    if bar_i >= 1:  # arpeggio enters with the data phase
        for e in range(8):
            note = chord[arp_pattern[e]] + 12
            pluck(bs + e * BEAT / 2, note, gain=0.115 if e % 2 == 0 else 0.085)

# Riser into the badge moment at 14.7 s
r_start, r_dur = 13.55, 1.15
n = int(r_dur * SR)
t = np.arange(n) / SR
f = 260 + 900 * (t / r_dur)
phase = 2 * np.pi * np.cumsum(f) / SR
add(r_start, np.sin(phase) * (t / r_dur) ** 2 * 0.05)
rng = np.random.default_rng(99)
add(r_start, rng.standard_normal(n) * (t / r_dur) ** 2 * 0.018)

# Impact boom at 14.7 s
n = int(1.1 * SR)
t = np.arange(n) / SR
f = 72 - 38 * (t / 1.1)
phase = 2 * np.pi * np.cumsum(f) / SR
add(14.7, np.sin(phase) * np.exp(-t * 4.5) * 0.7)

# Softer riser and impact into the investigation phase at 15.9 s
r_start, r_dur = 15.3, 0.6
n = int(r_dur * SR)
t = np.arange(n) / SR
f = 300 + 600 * (t / r_dur)
phase = 2 * np.pi * np.cumsum(f) / SR
add(r_start, np.sin(phase) * (t / r_dur) ** 2 * 0.035)
n = int(0.8 * SR)
t = np.arange(n) / SR
f = 68 - 30 * (t / 0.8)
phase = 2 * np.pi * np.cumsum(f) / SR
add(15.9, np.sin(phase) * np.exp(-t * 5.5) * 0.38)

# Gentle fade out at the end
fade_n = int(1.4 * SR)
out[-fade_n:] *= np.linspace(1, 0, fade_n)

peak = np.max(np.abs(out))
out = out / peak * 0.72
sf.write(str(Path(__file__).parent / "music.wav"), out.astype(np.float32), SR)
print("music.wav peak", float(peak), "bars", len(progression), "bar_s", BAR)
