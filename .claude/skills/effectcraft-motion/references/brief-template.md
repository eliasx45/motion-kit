# Brief template (v1, after R2 round 1)

The brief is the whole hand-off: a builder who never sees the reference must be able to rebuild
it from this alone. Write it before any code, also when you build yourself. The R2 loop tunes
this template; the version that scores best becomes the prompt expander's output format.

Rules for writing it:
- **Numbers, not adjectives.** Pixels (in a 1920 × 1080 frame), hex colours, frames at the comp's
  fps, percentages. "Big" and "fast" don't survive a hand-off.
- **Times as frames from the comp start** and, when there's a voice, relative to a word
  ("launch on 'CON' of content = f42, peak +2 f").
- One row per move. A move = one property of one element going from A to B.
- Say what is **not** there (no glow, no stroke, no background motion) when a builder might add it.
- Mark what you're unsure of; don't guess silently.
- **One source of truth per number** (R2 round 1, 22 Oct). Derive the moves table from the same
  measurements as the check table (`scripts/fit_graph.py` on the tracked values), or builders find
  they disagree and lose time choosing. When two targets can't both be met (a font size gives the
  right cap height but the wrong width), say which one wins.
- Say **how** a change is made when it could be several things: a dim row = opacity, not a colour
  change or a glow; which frame a colour was sampled at, and away from what.

## Describing a reference (what worked in R2, 22 Oct)

Blind builders matched a builder who saw the clip (86.8–87.1 vs 86.9) once the brief was:
1. **Tracked, not eyeballed.** Per-frame positions/scales of the moving group (rims, edges,
   a lattice fit for repeated cards), not a few hand-picked frames.
2. **Fitted.** `scripts/fit_graph.py` turns the track into moves: each one a null, two keys
   (frame: value), a Graph or a custom ease. Overlaps become stacked nulls.
3. **Short.** ~30–40 lines: picture (sizes, colours, fonts by measured width), states, the rig,
   one moves table, what's not there, one check line. Beats, pacing prose and long check tables
   added nothing (the 30-line brief scored best and built fastest).
4. **Mechanisms named:** opacity vs colour, what parents what, what zooms with the camera,
   motion blur and shutter, glow strength as "+N/255 next to it, gone by M px".
5. **The edges of the shot checked** (R2 r3, missed by the describer): the first and last frames
   are often transitions: a blurred / darker cut-in frame, a zoom + blur out. Compare frame 0's
   mean luma and sharpness with frame 2's.
6. **Each measurement validated by re-synthesis**: blur σ and zoom by warping + blurring a sharp
   frame until it matches (not a rim width a glow can contaminate); track with a method that
   survives motion blur (profile correlation), then fit. A describer error costs every builder
   the same points (r3: 56 for all three vs 76 for the control).

---

## 1. Comp
- Size, fps, length in frames, background (colour or gradient with stops and direction).
- Audio: file and where it starts; word timings with stressed syllables (frames).

## 2. Beats
| Beat | Frames | Words said | What the viewer should get |
|---|---|---|---|
| B1 | 0–41 | "…" | |

## 3. Elements
One block per element (or per repeated set):
- **Name** (as it should be in the comp: `B1 Card 0`), type (shape/text/precomp/placeholder).
- **Box**: centre x, y and w × h at rest (px); corner radius (px); rotation.
- **Look**: fill (solid hex, or gradient type + stops + direction; 4-Color Gradient points and
  colours for card bodies), stroke (none / hairline 1 px white 32 %), inner shadow (colour,
  opacity, size, distance, angle), other effects only if the reference has them.
- **Text**: content, font + weight (the nearest installed one if the reference's isn't), size
  (font size AND the measured width of each line, saying which wins), colour, tracking,
  alignment (left-aligned text needs `justify: "left"`), which word is coloured.
- **Edges:** an element cut off by the frame edge is just cut off; say so, or builders add a fade.
- **Parent** and layer order (what's above what).

## 4. Moves
| # | Element | Property | From → to | Start f | End f | Graph | Peak f | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | B1 Card 0 | position y | 1180 → 600 | 12 | 38 | Quick launch | 19 | 1 f cascade per card |

- Graph = one of: Fast In, Quick launch · soft landing, Smooth emphasis, Slow launch · quick
  finish, Fast out, Expo In-Out (Elias). Off→on / on→off / on→on decides most.
- Opacity fades with their own row (frames). Exits: fade ~8 f.
- Chained moves: say which overlap and by how much (next starts at ~60 % of the previous).
  Overlapping moves on one property = one row each, built on stacked nulls.
- A move that's already running when the shot starts (after a cut): give its real start before
  frame 0 (e.g. f −12), not a made-up start at 0.
- Camera moves / zooms: say what moves with them (the background too?).

## 5. Pacing summary
- Busiest moment (frame), longest hold, total number of distinct moves, how many things move at
  once at most. A one-line rhythm: "3 fast entrances in 1 s, 2 s hold, whip exit".

## 6. Not there
- Effects, glows, strokes, extra motion, camera moves the reference does NOT have.

## 7. Check targets
- Frames to compare (the 3–5 most telling), what must match there (positions ±4 px, colours
  ±6/255 per zone), peaks within 1 f of the listed frames, graphs 100 % matched.

## 8. Unsure
- Up to 3 choices you're least sure of, with your best guess.
