# DJ2 Trial Toggle: breakdown

**What it is:** a camera drops in on an app setting ("Trial" with its toggle on, and a **Post** button being tapped); a fan of thin light rays spreads from the button, then rows of Reels cards stack up above it, one beat at a time, while the camera pulls back in steps until the screen is a wall of reels.
**5.1 s, 1920×1080, 30 fps.** Background `#030303`.

Easing notation: `[speed, influence]`; influence is a fraction (`0.8` = 80 %). Speed 0 = soft start/landing. "out" leaves a key, "in" arrives at it.

## 1. Timeline

| Time (s) | What happens |
|---|---|
| 0.00–1.27 | Camera (CAM CTRL) drops from above: y −650 → 613.5, fast start (out 1500 px/s, 20 %), long soft landing (in 80 %). The UI comes down from the top; the ray fan is seen first as a crossed "lens" of curves |
| 0.50–1.00 | Ray fan opens: S2 2201.1 → 1927.2, S3 −617.5 → 1122.4, the curves uncross and become an open fan pointing down from the Post button (Asym −0.1 → −0.05 over 0.5–0.7) |
| 0.50–1.50 | Tap dot settles onto the right end of the Post button: (1228, 555) → (1207, 551), scale 90 → 100 % (out 20 %, in 90 %) |
| 1.27–1.63 | Hold |
| 1.63–5.07 | Camera keeps moving down (content slides down): 613.5 → 798.13 (2.43) → 993.48 (3.2) → 1001.03 (3.73) → 2960 (5.07, leaves at speed) |
| 1.67–4.47 | Camera zooms out in steps: 100 → 99.35 (1.67) → 93.89 (2.0) → 93.51 (2.57) → 78.65 (2.9) → 74.61 (3.3) → 54.44 (3.67) → 43.37 (4.47) |
| 1.93 | Reel grid row 1 pops on (hold key) |
| 2.43–3.80 | UI dims: 100 → 96.5 (2.67) → 88 (2.7) → 84.5 (2.9) → 82.5 (3.8) % |
| 2.73 | Row 2 pops on |
| 3.37 | Row 3 pops on |
| 3.83 | Grid floods to 24 rows (fills the frame) |
| 5.07–5.10 | Camera exits; end |

The zoom steps line up with the row beats: each new row is followed by a pull-back that makes room for it.

## 2. Elements

### Stage
| Layer | Look |
|---|---|
| BG (solid `#030303`) | Gradient Ramp, Radial, start `[960, 560]` `#0a0a0a` → end `[1960, 560]` `#050505`, Scatter 50 |

### Camera rig (null `CAM CTRL`)
`UI`, `Rays` and `Reel Grid` are parented to it (anchor `[0, 0]`), so its position is "where the UI centre is" and its scale is the zoom.

`transform/position` (x stays 960):
| t | y | out (leaving) | in (arriving) |
|---|---|---|---|
| 0 | −650 | [1500, 20 %] | |
| 1.2667 | 613.5 | hold to 1.6333 | [0, 80 %] |
| 1.6333 | 613.5 | [69.57, 58.3 %] | |
| 2.4333 | 798.13 | [21.18, 56.8 %] | [0, 99 %] |
| 3.2 | 993.48 | [0, 28.8 %] | [0, 90.9 %] |
| 3.7333 | 1001.03 | [240.19, 30.5 %] | [0, 62.4 %] |
| 5.0667 | 2960 | | [2619.97, 29.9 %] (still accelerating at the end: a whip out) |

`transform/scale` (uniform):
| t | % | in (arriving) | out (leaving) |
|---|---|---|---|
| 0 | 100 | | [0, 33 %] |
| 1.6667 | 99.35 | [−1.08, 99 %] | [−3.54, 69.8 %] |
| 2.0 | 93.89 | [−31.49, 20.7 %] | [−1.01, 16.5 %] |
| 2.5667 | 93.51 | [−10.12, 38 %] | [−0.52, 29.7 %] |
| 2.9 | 78.65 | [−7.66, 80.7 %] | [−14.41, 37.1 %] |
| 3.3 | 74.61 | [−18.7, 46 %] | [−34.47, 25.1 %] |
| 3.6667 | 54.44 | [−8.73, 99 %] | [−11.46, 37.9 %] |
| 4.4667 | 43.37 | [−1.22, 99 %] | |

### UI (precomp `DJ2 Trial Toggle - UI`, 1920×1080, motion blur on)
Positioned at `[0, 0]` under CAM CTRL. Opacity dims 100 → 82.5 % (keys above). Inside:

| Layer | Look |
|---|---|
| `Trial Icon` at `[656, 411]` | Dashed rounded square 68×68, roundness 18, stroke 4.5, dash 19.5 / gap 10.6 / offset −5; inside a rounded triangle (polygon, 3 points, radius 15, roundness 12, rotated 90°) stroke 4.5. White strokes |
| `Trial` at `[741, 429.5]` | SF Pro Display Medium 52, white |
| `Toggle` at `[1236.5, 410]` | Track 126×64, roundness 32; knob circle 50, white. **Rigged:** UI CTRL slider `Toggle` (0–1) drives track colour `linear(t, 0, 1, #4c4c54, #1385ff)` and knob x `linear(t, 0, 1, −31, 32.5)`. Here the slider is a static 1 (on) |
| `Post Button` at `[959.5, 540.5]` | 680×93, roundness 14, `#566afa` |
| `Post` at `[960, 556.5]` | SF Pro Display Medium 47, centred, white |
| `Tap` | Circle 74 with a radial gradient (centre → edge): `#6270fb` 0, `#6a8dff` 0.55, `#7ed8ff` 0.88, `#8ce8ff` 1.0. Moves `[1228, 555]` → `[1207, 551]` and scales 90 → 100 % over 0.5–1.5 s (out [0, 20 %], in [0, 90 %]) |
| `UI Haze` (Video off) | 860×230 r115 `#181a26`, Gaussian blur 150: a soft backlight, switched off in the final |
| `UI CTRL` (null) | Slider `Toggle` = 1 |

### Ray fan (`Rays` shape layer)
- 7 groups `Ray -3` … `Ray 3`, each a path built by an **expression** and a stroke `#ededf2`, width 2.5. Layer at `[0, −10.5]` (just under the Post button's centre).
- Expression, in plain words: ray number `k` (−3…3) is a curve from the apex `[0, 0]` straight down to an end point `L = 1600` px below. Its sideways spread is `w = k/3 × (1 ± Asym)`: outer rays spread most, the centre ray stays vertical, and `Asym` makes one side wider than the other. The end point sits at `x = w × S3`; the bend near the end is pulled sideways by `w × (S2 − S3)`; the start leaves straight down (tangent `L/3`).
  ```js
  var k=-3, L=1600, S2=effect("S2")("Slider"), S3=effect("S3")("Slider"), a=effect("Asym")("Slider");
  var w=k/3*(1+a*(k<0?-1:(k>0?1:0)));
  createPath([[0,0],[w*S3,L]], [[0,0],[w*(S2-S3),-L/3]], [[0,L/3],[0,0]], false)
  ```
- Three sliders on the layer animate the shape:
  | Slider | Keys |
  |---|---|
  | `S2` (bend) | 2201.1 at 0.5 (out 36.7 %) → 1927.2 at 1.0 (in 8.5 %) |
  | `S3` (end spread) | −617.5 at 0.5 (out 27.3 %) → 1122.4 at 1.0 (in 30.7 %) |
  | `Asym` | −0.1 at 0.5 → −0.05 at 0.7 (33 % / 33 %) |
  With S3 negative the ends land on the opposite side from the bend, so the curves cross (a lens shape); as S3 goes positive they uncross into a wide open fan.
- An **inverted mask** (rect x −860.7…743.3, y 1461…1613.1) cuts out the band where the ray ends land, so the tips never show.

### Reel grid (`Reel Grid` shape layer)
- One card: rect 293×474, roundness 12, fill `#1a1a21`, stroke `#d1d1d6` at 35 %, width 2.5, group at `[0, −449.6]` (above the UI).
- Repeater `Columns`: 7 copies, offset −3, step `[313, 0]` (a centred row from x −939 to +939).
- Repeater `Rows`: step `[0, −498]` (each row stacks **upward**), copies on **hold** keys: 0 → 1 (1.933) → 2 (2.733) → 3 (3.367) → 24 (3.833). Rows appear instantly on the beat, then the whole wall fills.

## 3. Knobs (if this comp were a template)

| Knob | Layer · property path | Current |
|---|---|---|
| Setting label | UI › `Trial` · text | "Trial" |
| Setting icon | UI › `Trial Icon` (shape; swap) | dashed square + play |
| Toggle state | UI › `UI CTRL` · `effects/#1/slider` (key it 0 → 1 to animate the switch) | 1 (on) |
| Toggle on / off colours | UI › `Toggle` · `contents/group#2/contents/fill/color` expression | `#1385ff` / `#4c4c54` |
| Button text | UI › `Post` · text | "Post" |
| Button colour / size | UI › `Post Button` · `contents/group/contents/fill/color`, `.../rect/size` | `#566afa`, 680×93 |
| Tap position / timing | UI › `Tap` · `transform/position`, `transform/scale` keys | (1228, 555) → (1207, 551), 0.5–1.5 s |
| Tap colours | UI › `Tap` · gradient fill colours | `#6270fb` → `#8ce8ff` |
| Ray count | `Rays` (number of `Ray k` groups, k = −3…3) | 7 |
| Ray length | `Rays` · `L` in each path expression | 1600 |
| Ray spread / bend / asymmetry | `Rays` · `effects/#1..#3/slider` keys | S2 2201.1→1927.2, S3 −617.5→1122.4, Asym −0.1→−0.05 |
| Ray colour / width | `Rays` · `contents/group*/contents/stroke/color`, `/width` | `#ededf2`, 2.5 |
| Card size / look | `Reel Grid` · `contents/group/contents/rect/size`, fill, stroke | 293×474, `#1a1a21`, `#d1d1d6` 35 % |
| Columns / spacing | `Reel Grid` · `contents/repeater/copies`, `/transform/position` | 7, 313 |
| Row spacing | `Reel Grid` · `contents/repeater#2/transform/position` | −498 |
| Row beats | `Reel Grid` · `contents/repeater#2/copies` hold keys | 1.933, 2.733, 3.367, 3.833 (→ 24) |
| Drop-in | `CAM CTRL` · `transform/position` keys 1–2 | −650 → 613.5 over 1.267 s |
| Zoom steps | `CAM CTRL` · `transform/scale` keys | 100 → 43.37 in 7 steps |
| Exit | `CAM CTRL` · last position key | 2960 at 5.067 |
| UI dim | `UI` · `transform/opacity` keys | 100 → 82.5 % |
| Stage colours | `BG` · `effects/#1/startColor`, `endColor` | `#0a0a0a`, `#050505` |

**21 knobs.**

## 4. Distinctive parts

| Name | What it is | From (layers · props) | Call it would enable | Overlaps |
|---|---|---|---|---|
| `rayFan` | Fan of thin curved rays from one point, rigged by 3 sliders, that opens from a crossed lens into an open fan | `Rays` (7 expression paths, sliders S2/S3/Asym, inverted mask) | `rayFan(comp, {from: [x, y], count: 7, length: 1600, at: 0.5, duration: 0.5, bend: [2201.1, 1927.2], spread: [-617.5, 1122.4], asym: [-0.1, -0.05], color: "#ededf2", width: 2.5})` | none |
| `toggleSwitch` | iOS-style switch whose colour and knob are driven by one 0–1 slider | UI › `Toggle` (expressions), `UI CTRL` · Toggle | `toggleSwitch(comp, {on: true, at, x, y, onColor: "#1385ff", offColor: "#4c4c54"})` | none |
| `settingRow` | A settings row: dashed-square "trial" icon + label + toggle | UI › `Trial Icon`, `Trial`, `Toggle` | `settingRow(comp, {label: "Trial", icon, on: true, x, y, width})` | uses toggleSwitch |
| `touchDot` | Gradient touch indicator (blue → cyan radial, 74 px) that drifts ~21 px onto a button and grows 90 → 100 % | UI › `Tap` | `touchDot(comp, {to: [x, y], at, duration: 1})` | proposals.json `cursorClick` (same job: show a press), different look: could be a `look: "touch"` option of it |
| `cardGridStack` | Wall of 9:16 cards built with two repeaters; rows appear one per beat (hold keys), then flood the frame | `Reel Grid` (repeaters `Columns`, `Rows`) | `cardGridStack(comp, {cols: 7, card: [293, 474], gap: [20, 24], rowsAt: [1.933, 2.733, 3.367], floodAt: 3.833, floodRows: 24, direction: "up"})` | `stagger` (rhythm) but instant row cuts, not entrances |
| `cameraDropIn` | Camera null drops the scene in from above: fast start, long soft landing | `CAM CTRL` · position keys 1–2 (−650 → 613.5, out 1500/20 %, in 80 %) | `cameraDropIn(comp, {cam, from: -650, to: 613.5, at: 0, duration: 1.2667})` | `slideUp` is the same curve idea for one layer; this moves the whole world down |
| `stepZoomOut` | Camera pulls back in steps, each step after a content beat, ending with a whip out | `CAM CTRL` · scale (100 → 43.37 in 7 keys), position (ends at 2620 px/s) | `stepZoomOut(comp, {cam, beats: [1.667, 2.0, 2.9, 3.3, 3.667, 4.467], scales: [99.35, 93.89, 78.65, 74.61, 54.44, 43.37], exit: true})` | proposals.json `cameraDrift` is a slow push; DJ3 `nullPullBack` is one fast pull-back; this is a stepped one synced to beats |
| `darkStage` | Near-black radial stage | `BG` (#030303 + Radial Ramp `#0a0a0a` → `#050505`, Scatter 50) | `background(comp, {look: "stage", center: "#0a0a0a", edge: "#050505", scatter: 50})` | same id as proposals.json `darkStage` |

## 5. Rebuild notes
- Everything is shapes, text and expressions: no footage, so it rebuilds fully (README: PASS ≥ 56 dB).
- **Fonts**: SF Pro Display Medium is a macOS font; elsewhere the labels fall back.
- The ray shapes exist only through the `createPath` expressions (their stored path is empty); if expressions are off, the rays vanish.
- BG's Gradient Ramp Scatter is seeded, so its grain differs by a level on rebuild.
- `UI Haze` (blurred backlight) is in the precomp but switched off; turn it on for a softer glow behind the UI.
- The toggle never animates here (slider is a static 1). Keying `UI CTRL` › Toggle 0 → 1 gives the switch-on move for free.
- `Tap` has no fade: it is visible from frame 0 (inside the UI that is still off screen).
- Scale values are stored with z = 0 (`[100, 100, 0]`); use `[x, y, 100]` from scripts.
