# Elias's taste: every rule with its value, date and why

Newest correction wins. Source files: `~/.claude/speech-edit/SYSTEM.md` (the agreed edit system),
the Claude memory folder for EffectCraft, lab R1 (`~/Developer/lab/R1-rsi-intro-exam/REPORT.md`).

## Contents
- [Graphs](#graphs)
- [Expo In-Out](#expo-in-out)
- [Timing on the voice](#timing-on-the-voice)
- [Overlap, holds and exits](#overlap-holds-and-exits)
- [Cards and tiles](#cards-and-tiles)
- [Post and reel cards](#post-and-reel-cards)
- [Pills and tags](#pills-and-tags)
- [Captions and on-screen text](#captions-and-on-screen-text)
- [Colour](#colour)
- [What he rejected](#what-he-rejected)

## Graphs

Motion Library → Devin Jatho → Graphs, 5 cards. The values are normalised After Effects temporal
ease on 2 keys: the move goes 0 → 1 over time 0 → 1, so speed is in units of the average speed
(Δv / Δt). The engine lists the same values: `keys.peakGraphs`.

| Graph | id (alignPeak) | first key out (speed, influence %) | second key in (speed, influence %) | peak at |
|---|---|---|---|---|
| Fast In | `fast-in` | 23.7527, 0.5927 | 0, 92.9214 | 0.1 % |
| Quick launch · soft landing | `quick-launch` | 0, 39.8783 | 0, 90.9238 | 26 % |
| Smooth emphasis | `smooth-emphasis` | 0, 70.2064 | 0, 70.0732 | 50 % |
| Slow launch · quick finish | `slow-launch` | 0, 83.0011 | 0, 60.1217 | 60 % |
| Fast out | `fast-out` | 0, 100 | 0, 0.8870 | 99.7 % |

- **Why** (22 Oct): Take 1 had good timing and layout and still "feels off cuz its not using my
  graphs from motion lib". The curves are a core part of what makes it his.
- Not the motion-library MCP's `curve_list` presets ("1", "fast slide in" ≠ his Fast In), not
  Easy Ease, not the kit's expo-out (0 / 100).
- One move's hand-tuned exception: the S2 05 card-row slide-up used out 11.5 % (speed 0) / in
  97.8 % (speed 0), landing key 26 f after launch for a 120 px rise (19 Oct). Reuse it only for a
  similar card-row slide-up; otherwise use the card.

## Expo In-Out

His saved curve for **on screen → another spot on screen** (a stage carry, a footage card
shrinking or changing sides, a dot running along a line). Motion Library `curve_presets`
e7e9542e…, bezier [0.8092, 0, 0.1752, 1], hand-shaped on the Tyson 20-08 Legends stage carry
(21 Oct). Not a Graphs card and not approved in the MCP.

- **Sharper the longer** (22 Oct): about 65 % on both sides for a 1 s move.
  Working formula (a fit, not confirmed by him): `out = clamp(65 + 30 (s − 1), 50, 90)`,
  `in = min(out + 1.5, 90)`: 0.5 s → 50, 1 s → 65, 1.5 s → 80, 2 s+ → 90. Speed 0 both sides.
  `expoInOut(d)` in graphs.jsx does this.
- Its peak sits mid-move, so a move that starts on its word peaks ~10 f later. Whether such moves
  should start earlier is an open question to him (22 Oct).

## Timing on the voice

- Speed peaks land on the **stressed syllable**: the peak sits about 2 frames after the consonant
  burst, i.e. the vowel − 1 frame. Reference: "CON-tent" = frame 1281 in his edit.
- Word and stress timings: `~/.local/bin/scribe-words` (ElevenLabs Scribe) for text; for
  frame-exact stress, `scripts/fork/speech-map` (Scribe → MFA → forward snap, 0.15 f median).
  You transcribe; never ask Elias to.
- Launch key on the stressed syllable's frame: with Fast In the speed peak lands ~1.75 f later.
- His top time sinks, which you must get right first: 1) timing and in/out, 2) size, position and
  overlaps, 3) what gets animated.

## Overlap, holds and exits

- **Overlap** (22 Oct): chained moves (exits → card move → entrances) overlap so the motion never
  fully stops. The next move starts at ~60 % of the previous one, past its peak. Keep the
  word-locked key on its word, shift the other end. An element never exits while its own entrance
  is still running.
- **Hold after landing**, no drift key (19 Oct: a drift key after a 120 px rise overshot on the
  auto-Bezier path, "moving up weirdly"). If a drift is ever wanted, make that key's spatial
  interpolation linear.
- **Exits fade out** over ~8 frames, never a hard cut (19 Oct). Exception: the cut also jumps to a
  clearly different zoom/shot, which hides it.
- Rows: 1-frame cascade left → right. Devin's landings are long: when unsure, a longer tail beats
  a shorter one (he moved a landing key 14 → 20 → 33 f).
- Pops: the Motion Library Bounce (`toolkit_bounce` {property, mode: overshoot, strength 20,
  frequency 3, decay 5}) on his selection, via `script.run`, restoring his selection after.

## Cards and tiles

From rebuilding the Surya and Moon Edits reference cards (22 Oct):

- **Body = a 4-Color Gradient**: "that's what he uses in his cards for the background, to have
  those points diagonally: black, and then the rest blue". A near-black point in one corner, blues
  in the others. In EffectCraft: effect `ec.generate.fourcolor` ("4-Color Gradient", points +
  colours + blend). In FigCraft (no 4-point gradient): a base fill + 4 stacked radial gradients
  fitted to the pixels (`~/Developer/lab/R1-rsi-intro-exam/figcraft/refcards/s1_refit.py`,
  ~3/255 mean error).
- **Inner shadows dark**, as dark as the reference measured per zone (the first rebuilds were too
  light on the diamonds and the $ card). A slightly blue body with a darker-blue inner shadow is
  the usual recipe (22 Oct, Moon search bar: "just a blue background … with an inner shadow
  that's slightly bluer or a darker blue").
- **A lighter patch around text or an icon is its glow, not the body.** Measure the body away
  from it and don't copy it as a fill or highlight (22 Oct: "Don't worry about the sort of glow
  that he made on the text. That's what's affecting what's around the text").
- **Rim:** brightness varies around the card. Sample it by angle; an angular-gradient stroke
  reproduces it.
- **Rounded triangles/shapes:** match the reference's corner radius by measuring row widths near
  the corners (he found the first triangle too sharp).
- **Hairline, not stroke:** 1 px on screen, white ~32 % (Devin's). A 3 px solid white stroke reads
  "very, very low quality" (19 Oct).
- The kit's hero gradient (`style.jsx` orb: #8bd2ff → #3a7bff → #1a1f6b) is "too flashy"
  (22 Oct). He is redesigning the look in FigCraft; until that lands, copy the reference.

## Post and reel cards

(19 Oct, S2 05, matched to Devin 6:22)
- Aspect **2:3** (card comp 320 × 480), never 3:4. Screenshot zoomed inside, track-matted.
- Corner radius **8.6 % of the card width**. Hairline as above.
- **Real screenshots only.**

## Pills and tags

His own finish (19 Oct, S2 05 VIRAL tags), the one glow he chose:
- Pill: Gradient Ramp red #FF0000 (top) → #FF2A2A (bottom); Deep Glow (Native): radius 116,
  exposure 0.01, spread 33, downsample 80, unmult on, dither 50, Screen; scale pop with the
  Motion Library Bounce.
- Pill text: the same Deep Glow + Drop Shadow (black, 100 %, 135°, distance ≈1.8, softness ≈2.8).
- Every pill gets Deep Glow + bounce; the ramp and the text stack were on Tag 0 only: build that,
  ask before copying to siblings.

## Captions and on-screen text

- Captions over the talking head: Motion Library preset **Elias/Text styles ▸ Caption glow + double
  shadow** (id 9a0c3382…). He scaled one to 133 %: build them bigger.
- On-screen text = the point, not a transcript: the takeaway or the twist, built as it's said,
  held once the thought is complete, then cleared. Colour only the word that carries the contrast.
- Important lines without a full animation get the spotlight `Text_Mid_video`
  (Devin Jatho → Text): reveal across the whole phrase, hold through pauses, text and dark
  background fade out together, no extras.
- Pattern interrupt about every 10–15 s (text counts, zooms don't).

## Colour

- 10-10 video (22 Oct): P01 Clock blues: navy `#0c1423`, mid `#236197`, bright `#4697f3` (accents),
  ice `#c5e4ff` (secondary text), white (main text). No red/green highlights there. Stroke taste
  for card/media frames in 10-10: 1 px, gradient white → dimmer white.
- Graphic-scene backgrounds: dark navy / near-black gradient (e.g. ramp [0.03, 0.09, 0.2] →
  [0.02, 0.05, 0.12] over #08080B). **Never purple** (18 Oct), never the presenter room photo.
- Client styles: Tapa = Devin style; Adrien = Tapa with blue → orange, nothing else.

## What he rejected

| Rejected | When | Instead |
|---|---|---|
| Glows the reference doesn't have | 22 Oct | copy only the reference |
| Kit hero gradients as "the look" | 22 Oct | his FigCraft design / the reference |
| Generic eases (Easy Ease, kit expo, MCP curves) | 22 Oct | his Graphs |
| Thick white card outlines | 19 Oct | 1 px hairline at ~32 % |
| Code-drawn placeholder images | 19 Oct | real images or a flat named placeholder |
| Drift keys after landing | 19 Oct | hold |
| Hard-cut exits | 19 Oct | 8 f fade |
| Purple | 18 Oct | dark navy |
| Learning from his old projects | 18 Oct | only the 8 reference comps and his picks |
