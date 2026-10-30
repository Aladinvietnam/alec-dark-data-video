# UI design layer, researched 30 October 2026

Added after the user judged the demo graphics flat and plain on 30 October 2026, with instructions to study UI design online and on GitHub and accumulate the lessons into the skill. Sources include the Open Props, Radix Colors, shadcn, Atlassian, Fluent 2, Material 3, Polaris, Carbon and Primer token systems on GitHub, published glass and glow recipes, Linear and Raycast teardowns, and Canvas 2D rendering practice for frame capture pipelines. Every value below is a working spec, not a mood.

## The background stack, in draw order

1. Base wash, a vertical gradient between two near black hues, never pure black. Default page base is the shadcn dark background hsl(222 84% 4.9%), close to #050810. Pure black kills shadow detail and makes gradients band.
2. Aurora or mesh blobs, three or four radial gradients with analogous hues only, each fading to transparent at the 65 to 70 percent stop. Peak alpha 0.10 to 0.22 for data graphics so the data always wins. One warm counter light blob at 0.10 alpha maximum. The brightest background area sits behind the hero element, because the background is a spotlight, not wallpaper.
3. A faded grid or dot field inside the plot area only, white at 2 to 6 percent alpha, cells 40 to 80 px, always faded out toward the frame edges with a radial mask. On maps a graticule every 10 to 15 degrees at 4 to 6 percent reads as a cartographic instrument. One grid or one dot field per frame, never both.
4. The data layer.
5. Film grain over the background and panels but under the text where the pipeline allows it, from pre-rendered noise tiles at 3 to 8 percent opacity in overlay blend, 3.5 percent being the shadcn standard. Grain doubles as dither, breaking the banding that 8 bit gradients and H.264 produce on dark scenes. Rotate four to six tiles across frames for animated film grain, and keep the grain static for data content and animated only for horror or VHS material.
6. A vignette baked on top, radial and elliptical, transparent until 55 to 70 percent of the radius, then darkening to rgba(0,0,0,0.35 to 0.5) at the corners.

## Surfaces and elevation

Depth comes from lightness steps before hue. Page at about 5 percent lightness, chart field at 8 to 9, panels at 11 to 13, a raised verdict card at 15, each separated by a hairline before any shadow is considered.

- Glass panel recipe. Fill white at 4 to 10 percent alpha, or a dark tint rgba(13,17,23,0.55 to 0.72) for heavy panels. Backdrop blur 12 to 20 px with saturate at 140 to 180 percent, because frost without saturation goes grey and dead. In Canvas, pre-render the background, draw it through a blur filter clipped to the panel path, then lay tint and border over it.
- Border. One px, drawn on a half pixel offset so it stays crisp, as a vertical gradient from white at 28 to 35 percent alpha at the top to 4 to 8 percent at the bottom, plus an inner top highlight line at white 12 to 20 percent. This gradient edge is the single clearest line between premium glass and a flat translucent card.
- Perimeter layer, from Atlassian. A 1 px stroke in a tinted dark colour at about 30 percent alpha around every raised card makes dark surfaces read as lifted without a visible drop shadow.
- Shadows. Black or tinted navy only, never coloured. Open Props dark recipe: shadow colour hsl(220 40% 2%) at 25 percent strength, layered with negative spreads, card level roughly 0 3px 5px at 28 percent plus 0 7px 14px at 30 percent. Fluent formula: every elevation is a key shadow whose blur equals the tier number with offset y at half the tier and 28 percent opacity in dark themes, plus an ambient shadow at 20 to 24 percent. A cheap three layer stack that reads well is blur 18 alpha 0.10, blur 10 alpha 0.16, blur 4 alpha 0.22, largest and faintest first. Bake panel shadows into sprites whenever the panel is static, because live shadowBlur is the most expensive Canvas operation.
- Radius ladder from one base. Base radius 8 px for chips, base plus 4 to 8 for cards at 12 to 16, large panels 20 to 24, pill at full round. Nested corners follow the shadcn derivation, outer radius minus the gap, so corners stay concentric.
- Bevel pairing, from Polaris and Open Props. Every drop shadow gets an inset bevel partner, a half px light line inside the top edge and a dark line inside the bottom edge, which is what makes a card look manufactured rather than drawn.

## The hero light

Only one element per frame earns full glow, the hero number, and the glow is in the data colour of that number.

- Floor wash first. A radial gradient in the accent at 8 to 14 percent alpha, radius two to three times the hero width, drawn before the hero, so the number appears to light the scene.
- Glow stack on the glyphs. Hot core in a near white tint of the accent, then a halo pass at blur 0.35 to 0.5 times the font size and alpha 0.45 to 0.6, then a bloom pass at blur 1 to 1.5 times the font size and alpha 0.18 to 0.3. Total bloom radius stays under about 1.5 times the cap height or the number turns to fog. Breathe the glow by crossfading a pre-blurred copy at plus or minus 10 to 15 percent opacity over two to four seconds, never by animating the blur radius.
- Gradient filled text. A vertical gradient across the glyph box with a hard mid stop pair near 45 and 55 percent reads as foil or metal, while a smooth ramp reads as airbrush. Gold hero example: #FFF6D8 at the top, #F5C542 at 45 percent, #C78F16 at 55 percent, #8A5E08 at the bottom, seated with a 1 px stroke of rgba(0,0,0,0.35). Gradient coordinates live in canvas space, so compute them from the measured text box and rebuild only when the box changes.
- Optional quarter resolution bloom pass for the whole scene. Draw the finished scene into a quarter size buffer through a bright pass filter, brightness 0.75 and contrast 2.2 to 2.8 with a 3 px blur, then add it back with the lighter composite at alpha 0.3 to 0.5. Apply it before titles and counters are drawn or text turns to fog.

## Typography system at 1920 by 1080

| Role | Size | Weight | Tracking | Notes |
|---|---|---|---|---|
| Hero number | 120 to 220 px | 700 to 800 | minus 0.02 em | Unit at 35 to 45 percent of the number size and 50 to 60 percent brightness |
| Verdict or secondary figure | 44 to 72 px | 700 | minus 0.01 em | |
| Title or claim line | 40 to 56 px | 600 to 700 | minus 0.01 to minus 0.022 em | |
| Kicker or section label | 20 to 26 px | 600 | plus 0.08 to plus 0.14 em | Uppercase, mono or sans |
| Data label | 22 to 28 px | 500 | plus 0.01 to plus 0.03 em | |
| Source line | 17 to 20 px | 400 to 500 | plus 0.04 to plus 0.08 em | Uppercase, muted |

Hierarchy steps differ by at least 20 to 25 percent in size or a full weight step, because near steps read as mistakes. The hero number stands at least four times its label size. Every counter and aligned figure uses tabular numerals or the mono font, because proportional digits jitter sideways while counting and read as a bug. One display family and one mono family per video, no more. Line height 1.0 to 1.1 on hero numbers and 1.25 to 1.4 on multi line text. Truncate labels, never numbers.

## Colour discipline

Surfaces stay desaturated and data carries the saturation. Neutral ramp, Tailwind zinc: page #09090B, panel #18181B, raised #27272A, border #3F3F46, secondary text #A1A1AA, primary text #F4F4F5. On the skill navy stage the same roles map to slate, page #020617, field #0F172A, panel #1E293B, border #334155, secondary text #94A3B8, primary text #F8FAFC.

Radix role mapping, which survives any hue swap. Step 9 is the solid hero colour designed to carry white text, step 10 its hover or grow state, step 11 low contrast label text, step 12 high contrast headline text, steps 3 to 5 card fills, steps 6 to 8 borders from subtle to strong.

One accent owns each scene as decoration, with semantic colours allowed only because they are data. The accent appears on an alpha ladder, 10 to 15 percent for washes, 25 to 35 for halos, 60 to 80 for borders and secondary marks, 100 only for the data itself. If everything is vivid, nothing is.

## Frame furniture, the instrument layer

- Corner ticks on the main panel or frame, L brackets with 14 to 24 px arms, 2 px stroke, white at 35 to 60 percent alpha or the accent at 70.
- Hairline dividers, 1 px at white 6 to 10 percent alpha, preferred over shadow gaps between zones.
- A source chip in a fixed corner of every data video, glass pill, mono uppercase text at 17 to 20 px, naming the source and the status of the number, such as SOURCE CHAINALYSIS, ESTIMATE.
- Status dots, 8 to 12 px with a halo at 25 to 35 percent alpha and three times the dot radius, green for live or confirmed, amber for estimate or pending, red for alert, pulsing by opacity only over 1.6 to 2.4 seconds.
- Fixed furniture positions across videos, a mono timestamp or frame counter, a title rule with a 24 to 40 px accent segment, so consistency of position becomes brand. At most four furniture elements per frame, and never fake detail such as random hex strings or decorative barcodes.

## Motion that feels expensive

- Default entrance curve is easeOutExpo, cubic bezier 0.16, 1, 0.3, 1, closed form one minus two to the power of minus ten t. Overshoot landings use easeOutBack at cubic bezier 0.34, 1.56, 0.64, 1 with about 8 to 10 percent overshoot, once per scene on the verdict element. Camera moves use easeInOutQuart, cubic bezier 0.76, 0, 0.24, 1.
- Entrances run 300 to 600 ms at UI scale and 800 to 1400 ms for camera pushes. Exits take about 75 percent of the entrance duration and ease in. Siblings stagger by 40 to 80 ms. Cheap motion is fast and linear, expensive motion is slower with a long tail, and bounce or elastic curves read as dated outside deliberate cartoon beats.

## Canvas production rules for this pipeline

- Bake everything static once, background plate with vignette, panel shadows, glow sprites, then stamp per frame. The renderer has a total wall clock budget, not a 16 ms frame budget, and shadowBlur is the most expensive mainstream Canvas operation, costing up to several times the frame time at radii above 20.
- Grain tiles are pre-rendered at 128 to 512 px and stamped with a pattern fill, one of the cheapest full screen operations, and the tile set rotates so the grain lives.
- Gradient objects are cached per element box and rebuilt only when the box changes.
- Chromatic fringe belongs to glitch and reveal frames only, the cheap tier being the text drawn three times with red and cyan copies offset 2 to 6 px under the white original with the lighter composite, always paired with horizontal slice offsets so it reads as signal damage rather than a print error.
- Lift the darkest gradient stop off pure black toward #080808 so the dither has levels to work with before the encoder sees the frames.
