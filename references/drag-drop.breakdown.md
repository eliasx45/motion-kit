# drag-drop: breakdown
(comp "Comp 7 - Script + screenshot drag and drop")

## 1. What it is
A hand cursor drags a file icon (a script, then a screenshot) into a Claude-style prompt box ("Good evening, OnlyTapa"). The icon shrinks into an attachment chip with its filename under it, and the hand opens and fades away.
**8.6 s (work area 0–3 s), 2142×1080, 30 fps.** Motion blur and frame blending are on.

> **Read this first.** The drag is meant to travel along a curved path, but in EffectCraft today the hand and icon stay still in the middle of the box. The path-following expressions fail with `TypeError: not a callable function` (section 6). So the GIF, and the README's "PASS", show the icons sitting at the centre with no travel, and the screenshot icon landing on top of the script icon. The numbers below describe the comp as authored. In After Effects it flies in from off-screen bottom right and lands at the left of the box, the second file 175 px to the right of the first.

## 2. Timeline
Main-comp times. The screenshot drop is the same precomp design, started 2.4667 s later.

| Time (s) | Beat |
|---|---|
| 0.00 | Prompt box on a slate background. The closed hand ("Grabbed") holds the **transcript icon** |
| 0.00–1.97 | **Drag**: hand + icon travel along a curve from off-screen bottom right (≈ [2514, 1626]) to the box (≈ [617, 512]). They start tilted about 55° and straighten as they land. Trace progress 100→0 (out infl 34.7, in infl 96.7: it covers most of the path early, then glides in) |
| 1.77–2.03 | Icon **shrinks** 16 → 6.8 % (ease in: out infl 100, in 33.3) |
| 2.03 | **Release**: the closed hand swaps to the open hand ("Grab") and the icon swaps to a settled copy. The **filename label** "transcript.docx" appears 65 px below the icon |
| 2.03–2.13 | Icon **settles up** 6.8 → 8.3 % |
| 2.00–2.17 | Open hand grows 24 → 38.3 % (it is already partway when it appears at 2.03) |
| 2.03–2.30 | Open hand tilts +3.77° → −3.73° |
| 2.13–2.40 | Open hand fades out (gone at 2.43) |
| 2.47–4.43 | **Second drag**: the **screenshot icon**, same moves, landing 175 px to the right |
| 4.23–4.50 | Screenshot icon shrinks. 4.50: release + "screenshot.png" label. 4.50–4.60: settles. 4.63–4.87: hand fades (gone at 4.90) |
| 4.90–8.60 | Hold: both attachments sit in the box |

## 3. Elements
Structure:
- The main comp holds two precomps of **5453×3068**: `01 Script - original timing` (start 0) and `02 Screenshot - original timing` (start 2.4667).
- Both are centred: anchor [2726.5, 1534] at [1071, 540].
- So precomp pixels = main-comp pixels, and the visible window is precomp x 1655.5–3797.5, y 994–2074.

### Stage and prompt box (Script precomp only; the Screenshot precomp is transparent above it)
| Layers | Look |
|---|---|
| `Dark Royal Blue Solid 6` (1920×1080 solid `#0e1214`, scaled 284 % to fill the precomp) | Gradient Ramp, **Radial**: start [960, 381] `#171919` → end [960, 1080] `#0e1214`. The centre sits high, behind the box. Scatter 0 |
| `claude.png` (footage 1448×1086, centred at [2727, 1534]) | A screenshot of the prompt box (greeting, input field, "+", model menu, mic). **Color Key**: key `#111519`, tolerance 10.7, removes the screenshot's own background. Plus a feathered (19 px) 15-point mask around the box, so it sits on the stage |

### Motion path rig (per precomp)
| Layer | What it does |
|---|---|
| `Shape Layer 1` (hidden, Script at [2726.5, 1510], Screenshot at **[2901.5, 1510]**) | Open 2-point path from [−453.9, −4.37] (the landing spot) to [1442.85, 1110.07] (off-screen bottom right). The handles make it a curve: vertex 2 in-tangent [−834.76, −1184.37], out-tangent [421.19, 597.59]. Stroke `#f7f7f7` at 68 %, 3 px, but the layer is hidden |
| `Trace Shape Layer 1: Path 1 [1.1]` (null) | **Trace Path** pseudo effect, `Progress` 100 @0 (out infl 34.7) → 0 @1.9667 (in infl 96.7). `Loop` is off; its loopOut("cycle") expression only runs with Loop on. **Position expression**: the point on the path at Progress/100, converted to comp space. **Rotation expression**: the path's direction there (`atan2` of the tangent), so the null turns to follow the curve: about 54.8° at the start, −3.77° at the landing spot |

Hand and icons are children of the trace null. Their own rotation of +3.77° cancels the null's −3.77° at landing, so they rest upright.

### Hand cursor
| Layers | Look | Motion |
|---|---|---|
| `Grabbed.png Comp 1` (precomp of a 512² PNG, closed hand), out 2.033 | at [87.2, −49.4] from the null, scale 38.3 %, rotation −2.73° (≈ 196 px on screen) | rides the null |
| `Grab.png Comp 1` (open hand), 2.033–2.433 | at [70.97, −44.51], rotation 3.77° | **Scale** 24 @2.0 (out infl 10.7) → 38.3 @2.167 (in infl 100). **Rotation** 3.77 @2.033 (out infl 10.7) → −3.73 @2.3 (in infl 100). **Opacity** 100 @2.133 → 0 @2.4 (infl 33.3 both: an even ease) |

### File icon (two copies swap at the release frame)
| Layers | Look | Motion |
|---|---|---|
| icon, out 2.033 (`transcript.png`, or the `Screenshot icon - matched 1254` precomp) | 1254² image, anchor centre, at [25.79, −15.83], rotation 3.77°, scale 16 % (≈ 200 px) | **Scale** 16 @1.767 (out infl 100 on x/y) → 6.8 @2.033 (in infl 33.3) |
| icon, in 2.033 | at [20.26, −19.03] (a 6 px jump at the swap) | same keys, plus → **8.3 @2.133** (infl 16.7 / 16.7): the settle-up |

### Filename label
| Layer | Look | Motion |
|---|---|---|
| `script.docx - attachment label` / `screenshot.png - attachment label` (text, in 2.033) | **Arial 18**, `#d9dee3`, centred. The text says "transcript.docx" (the layer name says script.docx) / "screenshot.png" | **Position expression** `L.toComp(L.anchorPoint) + [0, 65]` with L = layer 6 (the settled icon): it always sits 65 px under the icon's centre |

## 4. Knobs (if this were a template)
| Knob | Layer · path | Current |
|---|---|---|
| File 1 icon | Script precomp · `transcript.png` (both copies) | transcript.png (1254²) |
| File 1 name | `script.docx - attachment label` · Source Text | "transcript.docx" |
| File 2 icon | Screenshot precomp · `Screenshot icon - matched 1254` (precomp of screenshot-comp7.png) | 1254² icon |
| File 2 name | `screenshot.png - attachment label` · Source Text | "screenshot.png" |
| Number of files / spacing | one precomp per file; `Shape Layer 1` · `transform/position` x | 2 files, +175 px apart |
| Stagger | precomp layer `start` | 0, 2.4667 s |
| Drop box (UI screenshot) | `claude.png` + its Color Key `keyColor` / mask | Claude prompt box, key `#111519` |
| Entry curve / from where | `Shape Layer 1` path vertex 2 + tangents | off-screen bottom right |
| Drag duration | Trace `Progress` keys | 1.9667 s |
| Icon sizes | icon `transform/scale` keys | 16 → 6.8 → 8.3 % of 1254 px |
| Hand art | `Grab.png` / `Grabbed.png` | open / closed hand PNGs, 38.3 % |
| Label gap | label position expression `[0, 65]` | 65 px |
| Stage colours | `Dark Royal Blue Solid 6` · `effects/#1/startColor` / `endColor` / `start` | `#171919` → `#0e1214`, centre [960, 381] |

That is 13 knobs.

## 5. Distinctive parts
| Name | What it is | From | Call | Kit overlap |
|---|---|---|---|---|
| `pathCarry` | A null that follows a bezier path by a 0–100 progress value, turning to match the path's direction. Children are counter-rotated to land upright. Ease: out 34.7, in 96.7 (fast launch, long glide) | Trace null + `Shape Layer 1` | `pathCarry(layers, {from: [x, y], to: [x, y], bend, at, duration: 1.9667, orient: true})` | `cursorClick` (travel to a target); this adds a real curved path and auto-orient. Could be cursorClick's `drag` option |
| `handRelease` | Closed hand swaps to an open hand on drop; the open hand grows 24→38.3 % (0.17 s), tilts +3.77→−3.73° (0.27 s) and fades out (0.27 s) | Grabbed / Grab precomps | `handRelease(comp, {at, hand: "grab", parent})` | `cursorClick` (press dip; this is the drag-and-let-go version) |
| `dropIntoSlot` | Dragged item shrinks 16→6.8 % (ease in, out infl 100) over 0.27 s, swaps, then settles up to 8.3 % in 0.1 s: a file landing as a small chip | the two icon copies | `dropIntoSlot(layer, {at, from: 16, to: 6.8, settle: 8.3})` | `pop` (overshoot and rebound on the way in; this shrinks, then rebounds up) |
| `attachmentCaption` | A small centred filename (Arial 18 `#d9dee3`) that follows an icon at a fixed 65 px below it, by expression | label layers | `attachmentCaption(iconLayer, {text, gap: 65, at})` | `trailingLabel` (DJ3: a label that follows a text sideways) |
| `screenshotCutout` | A UI screenshot dropped onto the stage: its own background colour-keyed out (`#111519`, tolerance 10.7) and a feathered (19 px) mask around it | `claude.png` | `screenshotCutout(comp, {footage, keyColor, tolerance: 10.7, feather: 19})` | none |
| `dragDropAttach` (template) | The whole comp: one drop per file, staggered 2.4667 s, landing slots 175 px apart | everything | see the template proposal | — |
| `darkStage` (existing id) | Radial slate stage: `#171919` centred high at [960, 381], down to `#0e1214` at the bottom | BG solid | `background(comp, {look: "stage", center: "#171919", edge: "#0e1214", centerY: 381 / 1080})` | the existing proposal |

## 6. Rebuild notes
- **The drag doesn't play in EffectCraft.** The Trace null's Position and Rotation expressions reach the path as `pathLayer("ADBE Root Vectors Group")(1)("ADBE Vectors Group")(1)("ADBE Vector Shape")`, calling the layer like a function with match names. EffectCraft fails with `TypeError: not a callable function`, so the null stays at [2726.5, 1534].
  - Checked on the rebuilt project: at 1 s, `thisComp.layer("Shape Layer 1").content(1).content(1).path.pointOnPath(p)` works and returns [2584.3, 1532.3].
  - So either fix EffectCraft's layer-call syntax, or rewrite the two expressions with `.content(1).content(1).path`.
  - Until then, both drops land at the centre and overlap. That is what the GIF shows, and why the README's rebuild check passes: it compares two equally static renders.
- **Footage paths** point at Elias's Mac cache (`/Users/elias/Library/Caches/EffectCraft/Motion Library/blobs/…`): Grab.png, Grabbed.png, transcript.png, screenshot-comp7.png and claude.png. On another machine nothing but the background and labels renders.
- `Trace Path` is an After Effects pseudo effect (`Pseudo/ADBE Trace Path`, Progress + Loop) carried over as is. A kit primitive should use a plain slider.
- The label expressions pick the icon by **index** (`thisComp.layer(6)`), so reordering layers breaks them.
- The label text and the layer name disagree ("transcript.docx" vs `script.docx - …`).
- The open-hand scale key starts at 2.0, one frame before the layer's in-point (2.033), so it appears already partway grown.
- The prompt box's greeting and UI are baked into `claude.png`, not editable text.
