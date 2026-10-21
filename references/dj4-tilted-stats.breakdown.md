# DJ4 Tilted Stats — breakdown

Source: [`dj4-tilted-stats.recipe.json`](dj4-tilted-stats.recipe.json) ([gif](dj4-tilted-stats.gif)).
Proposals from this comp: [`dj4-tilted-stats.proposals.json`](dj4-tilted-stats.proposals.json).

## 1. What it is
Two reel cards (5.6M, 3.2M views) tilted in 3D drift toward the camera, then a hard cut to a
glowing blue progress ring counting up to 169K with "100 % Non-followers", while the cards
reappear on the left as a pixelated mosaic. **1920×1080, 30 fps.** The comp is 12.8 s long but
every layer ends at **2.8 s** and the work area is 0–2.8 s, so the real piece is **2.8 s**
(the rest is the background colour `#020203`).

Structure: main comp → 2 precomps.
- `DJ4 Tilted Stats - Cards` (2.8 s) is shown 0–1 s as a 3D layer through a 50 mm camera.
- `DJ4 Tilted Stats - Stats` (2.8 s) is shown 1–2.8 s (layer trimmed in at 1 s, so precomp time = comp time).
- `Eye` (80×56) wraps a PDF eye icon from the Motion Library, used next to every view count.

## 2. Timeline
| Time (s) | Beat |
|---|---|
| 0.00–2.80 | Faint horizontal scanline texture over everything (Venetian Blinds adjustment at 14.85 % opacity). |
| 0.00–1.00 | Tilted cards push toward the camera: z 296.5 → 270.5 (0.4 s) → 232 (1 s), linear (~65 px/s), with a tiny x/y drift. |
| 0.00–1.00 | Inside the cards precomp, Card L slides left 826.55 → 759.75 (eases out, still moving at 1 s), Card R stays: the pair spreads apart. |
| 1.00 | **Hard cut** to the Stats precomp + a blue haze. The cards are now flat, on the left, and pixelated (Mosaic). |
| 1.00–2.80 | Whole Stats layer slides left 1221 → 1131 (eases in, still moving at the end). |
| 1.00–2.80 | Ring fills 61.94 % → 89.6 % (counter-clockwise from 12 o'clock); the count above ticks 118K → 169K, updating 12 times a second. |
| 2.43–2.80 | A light sweep starts passing across the ring: center (960, 540) → (990, 560), width 44 → 70 (starts from rest, cut mid-move). |

## 3. Elements
| Element | Layers | Look | Motion |
|---|---|---|---|
| **Camera** | Camera 50mm (main) | Default 50 mm: zoom 2666.67, position (960, 540, −2666.67), no DOF | Static. |
| **Tilted cards (3D)** | Tilted Cards (precomp layer, 3D) | Rotation X −21.97°, Y 16.91°, Z 8.69°. Deep Glow Radius 116, Exposure 0.0174, Spread 33 (rest default) | `transform/position` keys (linear): 0 s (1498, 425.3, 296.5) → 0.4 s (1493.5, 424.5, 270.5) → 1 s (1494, 423.2, 232). Out-point 1 s. |
| **Reel card** (×2) | Card L / Card R (shape) + Views 5.6M / Views 3.2M (text, parented) + Eye (Library) L / R (Eye precomp, parented, scale 85.09 %) | Rounded rect 553.7×984.4, roundness 26, fill `#1a1a21`, 4 px stroke `#dbdee6`. Play button in the middle: ring Ø143.96 white stroke 4.98 px @ 35 %, triangle (3-point polygon, outer radius 35.99, rotated 90°, nudged x −5) white @ 45 %. Count: SF Pro Display Medium 62, `#ebebed`, tracking 20, at (−160, 440) from the card centre; eye icon at (−200, 418.16). | Card R static at (1236.85, 540). Card L `transform/position` 0 s (826.55, 540) → 1 s (759.75, 540): out speed 100 px/s @ 10 %, in speed 30 px/s @ 70 % — slow start, still drifting at the end. |
| **Stats block** | Stats (precomp layer) | Anchor (960, 542), **scale 118 % × 100 %** (everything inside is stretched 18 % wide) | `transform/position` 1 s (1221, 542) → 2.8 s (1131, 542): out 65 px/s @ 50 %, in 15 px/s @ 5 % (keeps moving to the end). |
| **Progress ring** | Ring Base, Ring Fill (shapes, in Stats), CTRL (null with slider "Progress") | Base: Ø201 ellipse, stroke `#1a1f25` 33 px. Fill: Ø201, gradient stroke 33 px `#2dbcff` → `#4fd0ff` (linear, (80, 80) → (−80, −80)), Trim Paths end = **Progress × 100**, layer scale −100 % × 100 % (mirrored, so it fills counter-clockwise). Deep Glow Radius 150, Exposure 0.02. CC Light Sweep direction 30°, sweep 60, edge intensity 40. Both at (960, 542). | Progress slider: 1 s 0.6194 (out speed 0.3/s @ 20 %) → 2.8 s 0.896 (in speed 0.06/s @ 33 %): a gentle ease, still creeping at the end. Light Sweep `center` 2.4333 s (960, 540) → 2.8 s (990, 560) and `width` 44 → 70 (out speed 0 @ 60 %, linear in). |
| **Count** | Count (text) + Eye (Library) (Eye precomp, scale 88 %, at (880, 377)) | SF Pro Display Medium 58, `#ebebed`, tracking 50, at (928, 397) | Source Text expression: *take the time, snap it down to 1/12 s steps (shifted 0.075 s), look 0.1 s ahead, read Progress there, × 190, round down, add "K"*. So 0.6194 → 0.896 shows 118K → 169K and the digits tick at 12 fps like a real counter. |
| **Legend** | Pct, Dot, Label (in Stats) | Pct "100%": Medium 58, `#ebebed`, tracking 50 at (1130, 539). Dot Ø12 `#0a8aeb` at (1139, 582). Label "Non-followers": Medium 36, `#787d85`, tracking 25 at (1157, 590). | Static (rides the Stats slide). |
| **Mosaic echo** | Mosaic (adj) (adjustment solid, Mosaic 56 × 31 blocks) over Reel Cards (shape), Title A, Title B (text) | Two flat cards 432×730, roundness 12, fill `#1a1a21`, 3 px stroke `#8c8f99`, play button (ring Ø112.32 @ 35 %, triangle r 28.08 @ 45 %) at x 569 and 188, y 475. Titles "Normal Reel" / "Trial Reel": Medium 50, `#bfbfc7`, centred, tracking −10, y 908. All pixelated into big blocks. | Static (rides the Stats slide). Carries the cards across the cut as an out-of-focus memory. |
| **Blue haze** | Haze Blue (solid, Add, parented to Stats) | Radial Gradient Ramp `#0f1b23` at (960, 542) → black at radius 850, layer scale 125 % × 100 % | Moves with the Stats block. In 1–2.8 s. |
| **Scanline texture** | Adjustment Layer 1 (adjustment, label Purple) | Venetian Blinds: completion 42.63 %, direction 90°, width 32.97, feather 91.4; layer opacity 14.85 % | Static, 0–2.8 s. |
| **Background** | BG (solid) | `#020203` | — |
| (hidden) | Eye (shape in Stats, video off); Eye + Pupil groups in Card L | Vector stand-ins for the eye icon (ellipse 52×33 stroke 7 + pupil Ø20; ellipse 46×30 stroke 6 + pupil Ø16) | Not visible; the PDF eye is what shows. |

## 4. Knobs (template)
| # | Knob | Layer › path | Current value |
|---|---|---|---|
| 1 | Left card views | Cards › Views 5.6M › `text/sourceText` | "5.6M" |
| 2 | Right card views | Cards › Views 3.2M › `text/sourceText` | "3.2M" |
| 3 | Ring progress from / to | Stats › CTRL › `effects/#1/slider` keys | 0.6194 → 0.896 |
| 4 | Count scale + suffix (count = progress × N) | Stats › Count › `text/sourceText` expression | × 190, "K" |
| 5 | Counter tick rate | Stats › Count expression | 12 per second |
| 6 | Percent text | Stats › Pct › `text/sourceText` | "100%" |
| 7 | Legend label | Stats › Label › `text/sourceText` | "Non-followers" |
| 8 | Legend dot colour | Stats › Dot › `contents/fill/color` | `#0a8aeb` |
| 9 | Ring colours | Stats › Ring Fill › gradient stroke colors | `#2dbcff` → `#4fd0ff` |
| 10 | Mosaic card titles | Stats › Title A / Title B › `text/sourceText` | "Normal Reel" / "Trial Reel" |
| 11 | Card tilt | Tilted Cards › `transform/rotationX/Y/rotation` | −21.97° / 16.91° / 8.69° |
| 12 | Push distance | Tilted Cards › `transform/position` z keys | 296.5 → 232 |
| 13 | Cut time / end | Tilted Cards out-point; Stats + Haze in/out | 1.0 s; 2.8 s |
| 14 | Haze colour | Haze Blue › `effects/#1/startColor` | `#0f1b23` |
| 15 | Card thumbnails (not used yet: cards are blank with a play button) | Card L / Card R, Reel Cards | none |

## 5. Distinctive parts
| Name | What it is | From | Call | Overlaps |
|---|---|---|---|---|
| `tiltedCardPush` | A precomp shown as a 3D layer, tilted (X −21.97°, Y 16.91°, Z 8.69°) through a 50 mm camera and pushed toward it at a constant ~65 px/s, with a soft Deep Glow | Camera 50mm, Tilted Cards | `tiltedCardPush(layer, {tilt: [-21.97, 16.91, 8.69], push: 64.5, at, duration: 1})` | `cameraDrift` (proposals.json) moves a camera rig; this tilts the layer itself |
| `reelCard` | 9:16-style reel placeholder: dark rounded card, light outline, translucent play button, eye icon + view count at the bottom | Card L/R + Views text + Eye (Library) | `reelCard(comp, {views: "5.6M", x, y, width: 553.7, play: true, footage?})` | same id as `reelCard` in DJ5 (adds eye + count); DJ1 `postCard` is the same family |
| `driftApart` | One card eases sideways away from its neighbour while the other holds, still drifting at the cut | Card L position (−66.8 px, out 100 px/s @ 10 %, in 30 px/s @ 70 %) | `driftApart(layer, {dx: -66.8, at, duration: 1})` | `slideUp` (that one enters and lands; this never lands) |
| `ringStat` | Progress ring: base ring + gradient fill whose trim end follows a slider, mirrored to fill counter-clockwise, glow and a light-sweep pass | Ring Base, Ring Fill, CTRL | `ringStat(comp, {from: 0.6194, to: 0.896, at, duration: 1.8, size: 201, width: 33, colors: ["#2dbcff", "#4fd0ff"]})` | same id as proposals.json `ringStat` |
| `countUp` | Slider-driven count, here progress × 190 + "K", ticking at 12 fps (stepped sampling) | Count expression | `countUp(textLayer, {from: 0.6194, to: 0.896, multiply: 190, at, duration: 1.8, suffix: "K", steps: 12})` | same id as proposals.json `countUp` (adds the `steps` option) |
| `statLegend` | Big percentage over a small coloured dot + grey label | Pct, Dot, Label | `statLegend(comp, {value: "100%", label: "Non-followers", color: "#0a8aeb", x, y})` | none |
| `mosaicEcho` | Previous scene's cards repeated flat and pixelated (Mosaic 56 × 31) behind the new stat, carrying them across a hard cut | Mosaic (adj) over Reel Cards + titles | `mosaicEcho(comp, {layers, blocks: [56, 31]})` | none |
| `settleSlide` | Whole block slides sideways and never quite stops (out 65 px/s @ 50 %, in 15 px/s @ 5 %): keeps a held shot alive | Stats position (−90 px over 1.8 s) | `settleSlide(layer, {dx: -90, at, duration: 1.8})` | `slideUp` (direction + no landing); related to `driftApart` |
| `lightSweep` | CC Light Sweep passing over the ring once: center (960, 540) → (990, 560), width 44 → 70, direction 30°, sweep 60, edge 40, starting from rest | Ring Fill `effects/#1` | `lightSweep(layer, {mode: "pass", at: 2.4333, duration: 0.3667, angle: 30, width: [44, 70], sweep: 60, edge: 40})` | same id as proposals.json `lightSweep` |
| `accentGlow` | Deep Glow Radius 150 / Exposure 0.02 on the ring fill (116 / 0.0174 on the tilted cards) | Ring Fill, Tilted Cards | `glow(layer, {radius: 150, exposure: 0.02})` | same id as proposals.json `accentGlow` |
| `hazeGlow` | Add-mode radial ramp (`#0f1b23` → black, radius 850, 125 % wide) parented to the content so the light travels with it | Haze Blue | `hazeGlow(layer, {color: "#0f1b23", radius: 850, stretch: 1.25})` | `background` / `darkStage` (that's the backdrop; this is a tinted light on top of it) |
| `scanlineTexture` | Very faint horizontal blinds over the whole frame (Venetian Blinds 42.63 %, width 32.97, feather 91.4, at 14.85 % opacity) | Adjustment Layer 1 | `scanlineTexture(comp, {opacity: 14.85, width: 32.97, feather: 91.4})` | none |

## 6. Rebuild notes
- **Missing footage:** the eye icon is a PDF from Elias's Motion Library cache
  (`/Users/elias/Library/Caches/EffectCraft/Motion Library/blobs/725b5e05…/Eye_White.pdf`). On any
  other machine it renders empty (no eye next to 5.6M / 3.2M / the count). The hidden vector Eye
  shapes in Stats and Card L could replace it.
- **Length:** the comp says 12.8 s but nothing exists after 2.8 s (work area 0–2.8 s). A template
  should be 2.8 s.
- The Stats precomp is stretched 118 % × 100 %, so the ring (drawn round, Ø201) shows slightly wide.
  Keep it if rebuilding exactly; a primitive should draw it round.
- The ring's light-sweep keys end at 2.8 s, exactly at the layer's out-point, so the pass is cut
  mid-move (by design or by trim).
- The count reads the slider 0.1 s ahead in 1/12 s steps; it ends on 169K although the slider's last
  value would give 170K.
- README rebuild check: PASS (no random seeds here).
