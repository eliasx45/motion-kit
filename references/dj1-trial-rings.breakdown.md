# DJ1 Trial Rings: breakdown

**What it is:** a vertical "flow chart" that the camera scrolls down. It starts at a blue "Trial Reels" tag with the Reels icon, follows a glowing dashed path to the **Non-Followers** ring (which lights up and fills 0 → 100 %), then follows a second path down to a post card ("693K" views) where a cursor lands on **Post**.
**6.3 s, 1920×1080, 30 fps.** Background `#050505`.

How to read the easing below: each keyframe has `out` (leaving it) and `in` (arriving at the next one) as `[speed, influence]`. Influence is a fraction: `0.33` = 33 %. Speed 0 means it starts or lands softly; `0.1667` (16.67 %) is After Effects' plain "linear-ish" default. A high in-influence (75–90 %) with speed 0 is a long, soft landing (expo-out feel).

## 1. Timeline

| Time (s) | What happens |
|---|---|
| 0.00 | "Trial Reels" blue tag already on screen; the whole world starts scrolling up fast (WORLD null) |
| 0.00–0.93 | Reels icon fades in under the tag (opacity 0 → 100) |
| 0.87–1.73 | Tag + icon group (ICON null) lifts 19.7 px |
| 1.00–2.20 | Tag + icon group shrinks 100 → 92.54 % |
| 1.10 | Scroll passes y −30.87 without stopping and keeps going |
| 1.33–2.63 | **Path A** (dashed, glowing) draws from the icon down to the left ring |
| 2.03–2.33 | CTRL **Active** 0 → 1: the Non-Followers ring, counter and label light up (from 11–15 % to 100 % opacity) |
| 2.23–3.90 | CTRL **Progress** 0 → 1: the ring fills clockwise-from-top (mirrored) and the counter counts 0 % → 100 % |
| 2.60–3.43 | Scroll holds: the two rings are centred |
| 3.40–4.07 | The two dim lower paths fade in (0 → 75 % by 3.53, → 100 % by 4.07) |
| 3.43–6.23 | Scroll continues down to the card (passes −1577.77 at 4.40, lands at −2135 at 6.23) |
| 3.80–5.53 | **Path C** (dashed, glowing) draws from the left ring down to the card |
| 4.23–5.83 | Cursor glides in from the lower right on a curved path to the Post button (on screen from ~4.97) |
| 5.10–5.63 | Cursor's parent nudges 16 px left onto "Post" (the "click" landing) |
| 6.23–6.30 | Hold on the card |

## 2. Elements

### Stage
| Layer | Look |
|---|---|
| BG (solid) | `#050505` |
| Haze (solid, **Add** blend) | Gradient Ramp, Radial, start `[960, 540]` `#050505` → end `[1960, 540]` `#000000`, Scatter 50: a faint centre lift |

### WORLD camera (null `WORLD`)
Every visible layer except BG/Haze is parented to `WORLD`; moving it is the "camera". `transform/position` (y only, x = 0):

| t | y | out [speed, infl] (leaving this key) | in [speed, infl] (arriving at this key) |
|---|---|---|---|
| 0 | 124.38 | [1126.9, 11.6 %] | |
| 1.1 | −30.87 | [178.9, 51.5 %] | [178.9, 37.1 %] (same speed in and out: no stop) |
| 2.6 | −972 | (same value until 3.4333: a hold) | [0, 74.7 %] |
| 3.4333 | −972 | [0, 78 %] | |
| 4.4 | −1577.77 | [1286.6, 25.6 %] | [1286.6, 6.6 %] (passes through at full speed) |
| 6.2333 | −2135 | | [0, 45 %] |

So: a fast start, a soft landing on the rings, a pause, a slow-out then a long glide to the card.

### Title tag + icon (null `ICON`, children `Trial Reels`, `Label BG`, `Reels Icon`)
- **Label BG**: rect 521×101, roundness 4, at `[956.5, 419.5]`, fill `#2a8efd`, Deep Glow.
- **Trial Reels**: SF Pro Display Bold 107, centred, white, at `[958, 460]`.
- **Reels Icon**: one shape group made of a rounded square 369×368 (roundness 100) at `[959.5, 682]`, minus (Merge Paths: Subtract) a 400×34 bar at y 599, two slanted parallelograms (the clapper stripes) and a 3-point rounded polygon (radius 80, roundness 18, rotated 90°, the play triangle) at `[950, 716]`. White fill, Deep Glow. Opacity 0 → 100 over 0–0.933 s (out [27, 22.5 %], in [0, 92.8 %]).
- **ICON null** (anchor `[959.5, 682]` = icon centre): position y 682 → 662.3 over 0.867–1.733 (out 77.6 %, in 30.6 %); scale 100 → 92.54 % over 1.0–2.2 (out 62.3 %, in 53.2 %).

### Dashed paths (`Path A`, `Path C`, and the ghosts in `Inactive (dim)`)
- S-curves made of 2 vertices with vertical tangents (−290 / +290 or +320), so they leave straight down and arrive straight down.
  - Path A: `[925, 866]` → `[652, 1345]` (icon → left ring). Dash offset 23.
  - Path C: `[684, 1800]` → `[958, 2336]` (left ring → card). Dash offset 41.
- Stroke white (default), width 20, dashes: dash 42, gap 40.5. Deep Glow.
- Draw-on = **Trim Paths end** 0 → 100:
  - Path A 1.333–2.633 s: out [43.5, 72.6 %], in [0, 75.5 %] (starts already moving, long soft landing).
  - Path C 3.8–5.533 s: out [4, 54.2 %], in [0, 87.3 %].
- **Ghost paths** (`Inactive (dim)` layer, same geometry, `#161616`/`#171717`, width 20, same dashes): the four full paths (A, B to the right ring, C, D) always visible underneath so you see the route before it lights up. The lower pair (C dim, D dim) is in group `Lower paths` whose opacity is 0 → 75 (3.4–3.533) → 100 (4.067).

### Rings (`Ring L Base`, `Ring L Fill`, `Counter L`, `Non-Followers`; right side in `Inactive (dim)`, `Counter R`, `Followers`)
- Left ring centre `[653, 1525]`, right ring centre `[1267, 1525]`, diameter 344, stroke 22.
- **Ring L Base**: stroke `#646464`. Opacity expression `11 + 89 * Active` (11 % until lit).
- **Ring L Fill**: gradient stroke, linear top→bottom (`[0, −172]` → `[0, 172]`), white → `#dcdcdc`, width 22. Trim end expression `Progress * 100`. Scale **−100 %** horizontally, so it fills counter-clockwise (mirror of the default). Deep Glow.
- **Counter L**: Source Text expression `Math.round(Progress * 100) + "%"`; Chalkduster 94, centred, at `[651, 1557]`, scale **68 % × 100 %** (horizontally squeezed: a hand-written, condensed look). Opacity `15 + 85 * Active`.
- **Non-Followers**: SF Pro Display Medium 54, centred, white, at `[654, 1775]`; opacity `15 + 85 * Active`.
- Right side stays "off": ring track `#131313`, Counter R "0%" `#161616` (same font/scale), Followers `#2c2c2c`.

### Controller (null `CTRL`)
Two sliders drive everything about the ring:
| Slider | Keys | Drives |
|---|---|---|
| `Active` (effects/#1) | 0 at 2.033 (out 10.3 %) → 1 at 2.333 (in [14.6, 22.4 %]) | opacity of base, counter, label |
| `Progress` (effects/#2) | 0 at 2.233 (out 57.1 %) → 1 at 3.9 (in 80.8 %) | ring trim end and counter text |

### Post card (`Card`, `693K`, `Eye (Library)`, `Post`)
- `Card` shape: card 383×675, roundness 14, centre `[958.5, 2673.5]`, fill `#1c1c20`, stroke `#7a7a7a` 2.5. Under it: Post button 205×67 r12 at `[870.5, 3062.5]` `#077ae6`; Trash button 113×67 r12 at `[1092.5, 3062.5]` `#be171b` with a white trash glyph (3 small rects). A shape-drawn eye group exists but is **disabled** (the library Eye is used instead).
- `693K`: SF Pro Display Bold 77 at `[909.068, 2706]`, white. `Eye (Library)`: precomp of a white eye PDF (80×56) at `[852.068, 2680]`, scale 115 %.
- `Post`: SF Pro Display Medium 42, centred, `#dce9f7`, at `[872, 3073]`.

### Cursor (`Cursor` null-like shape + `Cursor (Library)` precomp)
- `Cursor` (shape, **Video off**, so invisible): it is just the parent/target. Position `[962, 3074]` → `[946, 3069]` over 5.1–5.633 (in 85 %). Its own ellipse/Deep Glow/opacity keys (0 → 100, 5.067–5.4) don't render.
- `Cursor (Library)`: precomp of a cyan cursor PDF (112×112), scale 75 %, parented to `Cursor`. Position (relative to parent) `[144.62, 288.41]` → `[0, 0]` over 4.233–5.833, out [0, 40 %], in [0, 80 %], curved motion path (spatial out tangent `[0, −158.6]`, in tangent `[79.5, 0]`): it rises and then hooks left onto the target.

## 3. Knobs (if this comp were a template)

| Knob | Layer · property path | Current |
|---|---|---|
| Title text | `Trial Reels` · text | "Trial Reels" |
| Title tag colour | `Label BG` · `contents/group/contents/fill/color` | `#2a8efd` |
| Title tag size | `Label BG` · `contents/group/contents/rect/size` | 521×101 |
| Hero icon | `Reels Icon` (whole shape layer; swap for any icon/footage) | Reels glyph |
| Active branch label | `Non-Followers` · text | "Non-Followers" |
| Inactive branch label | `Followers` · text | "Followers" |
| Inactive counter | `Counter R` · text | "0%" |
| Final percentage | `CTRL` · `effects/#2/slider` (2nd key) | 1 (= 100 %) |
| Counter suffix / format | `Counter L` · `text/sourceText` expression | `Math.round(P*100) + "%"` |
| Counter font + squeeze | `Counter L`/`Counter R` · font, `transform/scale` | Chalkduster 94, 68 × 100 % |
| Which side is active | positions of `Ring L *`, `Counter L`, `Non-Followers`, `Path A`, `Path C` vs. the dim set | left |
| Ring colours | `Ring L Fill` gradient stroke; `Ring L Base` · `contents/stroke/color` | white → `#dcdcdc`; `#646464` |
| View count | `693K` · text | "693K" |
| Count icon | `Eye (Library)` (footage) | eye PDF |
| Button label | `Post` · text | "Post" |
| Button colours | `Card` · `contents/group#3/contents/fill/color`, `contents/group#2/contents/fill/color` | `#077ae6`, `#be171b` |
| Card colour / stroke | `Card` · `contents/group#5/contents/fill/color`, `.../stroke/color` | `#1c1c20`, `#7a7a7a` |
| Cursor art | `Cursor (Library)` (footage) | cyan cursor PDF |
| Path draw timing | `Path A`, `Path C` · `contents/trim/end` keys | 1.333–2.633, 3.8–5.533 |
| Light-up / fill timing | `CTRL` · `effects/#1/slider`, `effects/#2/slider` keys | 2.033–2.333, 2.233–3.9 |
| Scroll stops | `WORLD` · `transform/position` keys | 124.38 → −972 (hold 2.6–3.43) → −2135 |
| Glow strength | Deep Glow on 7 layers · Radius, Exposure | 150, 0.02 |

**21 knobs.**

## 4. Distinctive parts

| Name | What it is | From (layers · props) | Call it would enable | Overlaps |
|---|---|---|---|---|
| `dashedConnector` | Glowing dashed S-curve that draws itself from one node to the next, over a dark "ghost" copy of the same route | `Path A`/`Path C` (path, stroke 20, dash 42/gap 40.5, trim end), `Inactive (dim)` ghosts, Deep Glow | `dashedConnector(comp, {from: [x, y], to: [x, y], at, duration, ghost: true, width, dash, gap})` | none (no line/path primitive in the kit) |
| `ringStat` | Progress ring (base + gradient fill, trim = Progress × 100, mirrored) with a counter and label | `Ring L Base`, `Ring L Fill`, `Counter L`, `Non-Followers`, `CTRL` Progress | `ringStat(comp, {value, label, at, duration, size, x, y})` | existing proposal `ringStat`; uses `countUp` |
| `countUp` | Text that counts from a CTRL slider: `Math.round(P*100) + "%"` | `Counter L` · `text/sourceText`, `CTRL` · Progress | `countUp(textLayer, {from, to, at, duration, suffix: "%"})` | existing proposal `countUp` |
| `focusBranch` | One "Active" slider lights a chosen branch (opacity 11–15 % → 100 %) while the alternative stays dark grey: "this one, not that one" | `CTRL` · Active; opacity expressions on `Ring L Base`, `Counter L`, `Non-Followers`; dim colours on the right side | `focusBranch(activeLayers, {at, duration: 0.3, dimOpacity: 15})` | DJ5 `dimAway` is the inverse (loser fades back) |
| `scrollStops` | A WORLD null that scrolls the whole scene vertically, stopping on each stage (fast start, soft land, pause, long glide) | `WORLD` · `transform/position` | `scrollStops(comp, {stops: [{y, at, hold}], world})` | none (different from proposal `cameraDrift`, which drifts/pushes; this is a stop-and-go vertical scroll) |
| `titleTag` | Bold white title on a flat colour highlight block (tight 4 px corners), glowing | `Label BG`, `Trial Reels` | `titleTag(comp, {text, color, x, y, size})` | none |
| `liftSettle` | After an element appears, it lifts a few px and shrinks to ~92.5 % to make room for what follows | `ICON` null · position (−19.7 px, 0.87–1.73), scale (100 → 92.54, 1.0–2.2) | `liftSettle(layer, {at, lift: 19.7, scale: 92.54, duration})` | close to the tail of `pop`/`slideUp` but a separate "make room" beat |
| `reelsGlyph` | The Reels app glyph built from shape boolean ops (rounded square − bar − stripes − play triangle), white with glow | `Reels Icon` | `reelsGlyph(comp, {size, x, y})` | `orb` (another hero shape), but a different look |
| `postCard` | Dark social post card with eye + view count and Post / Trash buttons | `Card`, `693K`, `Eye (Library)`, `Post` | `postCard(comp, {views: "693K", button: "Post", x, y})` | none |
| `cursorClick` | Cursor glides in on a curved path and lands on a button | `Cursor` (target, nudge 16 px), `Cursor (Library)` (curved travel 4.23–5.83, scale 75 %) | `cursorClick(comp, {to: layer, from, at, travel})` | existing proposal `cursorClick` |
| `accentGlow` | Deep Glow, Radius 150, Exposure 0.02, Spread 33 on every accent (paths, ring fill, tag, icon) | Deep Glow on 7 layers | `glow(layer, {radius: 150, exposure: 0.02})` | existing proposal `accentGlow` |
| `darkStage` | `#050505` solid + Add-mode radial haze `#050505` → `#000`, Scatter 50 | `BG`, `Haze` | `background(comp, {look: "stage"})` | existing proposal `darkStage` |

## 5. Rebuild notes
- **Library footage is missing outside Elias's Mac**: `Eye (Library)` and `Cursor (Library)` point to PDFs in `/Users/elias/Library/Caches/EffectCraft/Motion Library/blobs/…` (`Eye_White.pdf`, `Cursor_Cyan.pdf`). Without them the eye and the cursor simply don't show (seen in a rebuild here). The card's own shape eye group is disabled; enable it as a fallback.
- **Fonts**: Chalkduster (counters) and SF Pro Display (all other text) are macOS fonts; elsewhere they fall back and the counter loses its chalky look.
- **Deep Glow** is stored as a raw third-party effect (`ec.stylize.deepglow`, PEDG params); it rebuilds in EffectCraft but is the first thing to check if glows look off.
- Haze's Gradient Ramp Scatter is seeded, so its noise differs by a level or two on rebuild.
- The `Cursor` shape layer is hidden (Video off) but still carries a Deep Glow, a fill and opacity keys: they do nothing visible; only its position matters (it's the parent).
- `Cursor (Library)` has a zero-length open mask (no effect).
- Scale values are stored with z = 0 (`[100, 100, 0]`); use `[x, y, 100]` when setting them from scripts.
