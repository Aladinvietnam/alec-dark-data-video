# Alec-style dark data video

## Scope and independence

- Keep this skill fully separate from the morning tech news channel skill and do not import its light theme, its two host voices or its long form structure.

- Make one video for one data story and let one claim carry the whole video.

- Read [the Alec reference notes](references/alec-reference-videos.md) before the first video in a new topic area and compare the draft against those notes at check time.

## Choose one template

- Pick the map tour when the story moves across places and each stop adds one label and one number.

- Pick the chart duel when the story is a fall, a rise or a size comparison and one bar or line must visibly beat or collapse against a known benchmark.

- Pick the count and board when several countries or actors do the same thing and a rising counter plus a closing summary board gives the payoff.

- Pick the target lock when the whole story sits in one hotspot, and zoom the map into that strait, border or facility while a route, a target ring and one very large red count carry the danger.

- Pick the evidence collage when one frame must hold a main chart beside an ownership or flow diagram and several small falling charts, and land a red verdict stamp over the sanctioned side at the end.

- Pick the screen grid when the story is about an alert or a broadcast reaching everyone, and open on a grid of glowing screens with teal as the lead colour before the coverage counter lands.

- Pick the arc and card when money or goods move between exactly two places, and draw one gold arc, zoom into the destination and land one large holding card there.

- Use a real speech clip with a map behind it only when the user supplies or approves that exact clip and its subtitles.

## Verify and distill the data

- Verify every number from its primary source before drawing anything and record the source beside each number in the working notes.

- Drop any item that has no reachable source and tell the user which item was dropped and why.

- Reduce the story to one claim title, one hero number, and three to seven supporting labels in reading order.

- Put the fuller investigation in the post caption and keep the video text short enough to read while muted.

- Write the claim title as a plain statement a viewer can judge, such as a comparison or a warning, and never as a question with no answer in the video.

## Design the single canvas

- Build the canvas at 1920 by 1080 and 30 frames per second and design the horizontal layout from the start.

- Hold one visual plane for the whole video, either a dark map or a dark chart, and avoid cutting away to unrelated scenes.

- Use a deep navy background with slowly drifting aurora glows in violet, blue and teal plus fine star dots, added by decision of the user on 30 October 2026, and keep a dark vignette so text stays readable.

- Keep the aurora saturation and the bar gradients vivid enough that the frame feels colourful at first glance, strengthened by decision of the user on 30 October 2026, and balance the extra brightness by dimming the chart behind any panel that opens over it.

- Use a bold sans serif in uppercase for titles, labels and numbers.

- Use white for titles, gold for the hero number and the main route, red for loss, danger and sanctions, and teal for frozen, secured or covered amounts and for preparedness and emergency topics.

- Put each bar value inside its bar in a contrasting colour once the bar is tall enough, so the viewer reads the amount from the bar itself and not only from the hero number.

- Give the main bars a soft glow in their own colour so the colour coding stays readable against the dark background.

- Keep the title fixed at the top and keep any counter fixed in one corner so the viewer always knows the claim and the progress.

- Lay the canvas out on fixed zones for the header, the hero number, the chart, the subtitle line, the verdict row and the closing cards, and keep each element inside its own zone.

- Measure text widths in code and lay multi item rows out from the measured widths with a fixed gap, and shrink any line that would exceed its zone until it fits, so no two texts ever touch or overlap.

- Keep the user interface refined with pill chips, hairline dividers, glass cards with one accent bar and one corner radius used everywhere.

- Add a small flag chip only where place identity matters and keep every label clear of the hero number.

## Animate the data itself

- Move the camera with one slow pan or one slow zoom across the map or chart and let that movement reveal the stops in order.

- Open a warning story with a clear alert effect, such as a pulsing symbol with expanding rings and a breathing red border, and remove it before the data phase starts.

- Add an investigation phase after the hero reveal when the user asks for cause analysis, and present it as an evidence board panel over the dimmed chart with a numbered timeline of two to three findings that slide in one by one.

- Head every investigation finding with its source and mark the whole panel as early findings when the cause is suspected and not confirmed, and phrase each finding as a question or a suspicion until a primary source confirms it.

- Grow bars with a slight overshoot so the landing is visible, and mark the verdict moment with a brief white flash and an expanding ring around the badge.

- Push the camera in slowly across the whole video on top of the single pan or zoom, keeping the push small enough that no label leaves the frame.

- Animate the data directly by counting numbers up or down, drawing routes, growing bars, dropping chart lines and revealing labels one by one.

- End a chart duel with a stamp, a verdict word or a multiple badge placed over the losing or sanctioned side.

- End a count and board video on the full summary board and hold that board long enough to read.

- Render a 3 to 7 second test first, inspect frames at each change point, and confirm the data itself moves before rendering the full video.

- Reject a still image with a slow zoom presented as animation and rebuild the scene so the numbers, lines or labels change on screen.

## Sound and timing

- Use one narrator voice in the language of the post, added by decision of the user on 30 October 2026, and keep the video fully readable with sound off as well.

- Write the narration as short segments that match the animation phases one to one, record each segment on its own, and build the timeline from the measured length of each segment plus a short pad.

- Spell numbers out in words in the narration script so the voice reads amounts correctly, and keep place and company names in their original form.

- Show a subtitle line for each narration segment while its phase runs, and let the closing verdict line and cards carry the last segment instead of a subtitle.

- Compose an attractive background track for each video with a chord progression, a pulsing bass and kick, and an arpeggio that enters with the data phase, and place a riser and an impact hit exactly on the verdict moment.

- Keep the music low under the voice and let the voice carry the timing of every reveal.

- Target 8 to 28 seconds for a pure data clip, allow up to about 36 seconds when narration and an investigation phase are added, and give each label at least 1.5 seconds on screen.

- Give the hero number the largest size and the longest hold of any element in the video.

## Render and check quality

- Draw the scene in HTML and Canvas with JavaScript, capture frames with Playwright and Chromium, and assemble the video with ffmpeg.

- Wait for fonts to load before capturing frames and embed images as data URIs when a capture script needs local files.

- Check the finished file with ffprobe for duration, resolution and frame rate before delivery.

- Extract frames at the opening, at each data change and at the closing board, and inspect them for overflow text, overlapping labels, wrong flags and numbers that do not match the verified notes.

- Check that no frame presents a reported plan as a signed deal, an estimate as a measured result, or an illustration as a real photo.

- Deliver the video with its duration, its template name, and the verification status of its numbers.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.
