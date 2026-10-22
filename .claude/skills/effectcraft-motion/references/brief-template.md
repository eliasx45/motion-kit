# Brief template (v0)

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
- **Text**: content, font + weight, size (px cap height or font size), colour, tracking,
  alignment, which word is coloured.
- **Parent** and layer order (what's above what).

## 4. Moves
| # | Element | Property | From → to | Start f | End f | Graph | Peak f | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | B1 Card 0 | position y | 1180 → 600 | 12 | 38 | Quick launch | 19 | 1 f cascade per card |

- Graph = one of: Fast In, Quick launch · soft landing, Smooth emphasis, Slow launch · quick
  finish, Fast out, Expo In-Out (Elias). Off→on / on→off / on→on decides most.
- Opacity fades with their own row (frames). Exits: fade ~8 f.
- Chained moves: say which overlap and by how much (next starts at ~60 % of the previous).

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
