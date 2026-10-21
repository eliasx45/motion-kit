# DJ3 Views Counter — breakdown

Source: [`dj3-views-counter.recipe.json`](dj3-views-counter.recipe.json) ([gif](dj3-views-counter.gif)).
Proposals from this comp: [`dj3-views-counter.proposals.json`](dj3-views-counter.proposals.json).

## 1. What it is
A "Professional dashboard" stat card sitting on a phone screen: the camera pulls back fast from a
close-up while the frame snaps into focus and a green ↗ arrow + counter races from 6.8M to 42.8M
"views in the last 30 days". **4.27 s, 1920×1080, 30 fps**, comp background `#020202`.

The whole scene hangs off one null, **CAM CTRL**: every visible layer except Defocus and BG is
parented to it, so scaling the null is the "camera". The same null holds the counter's slider.

## 2. Timeline
| Time (s) | Beat |
|---|---|
| 0.00–0.30 | Whole frame snaps into focus: Defocus blur 40 → 0 (fast, nearly linear, still moving when it lands, so it "clicks" sharp). |
| 0.00–2.17 | Camera pull-back: CAM CTRL scale 195.81 % → 104.074 %. Launches at full speed, then a very long glide (expo out). |
| 0.00–1.93 | Counter 6.8M → 42.8M on the same kind of curve: most of the count happens in the first 0.4 s (29.8M at 0.40 s, 36.6M at 0.77 s, 42.2M at 1.53 s). |
| 0.00–4.27 | "views in the last 30 days" stays glued 15 px right of the number as its width changes. Arrow's light sweep shimmers the whole time (wiggling angle). |
| 2.17–4.23 | Slow creep: scale 104.074 % → 100 %, *accelerating slightly* (−0.46 %/s → −5.5 %/s), so the shot is still moving at the cut. |

## 3. Elements
Positions of children are in CAM CTRL's space: the null sits at (960, 540) with anchor (50, 50), so a
child at (50, 50) is screen centre at 100 % scale.

| Element | Layers | Look | Motion |
|---|---|---|---|
| **Camera rig** | CAM CTRL (null, hidden) | Effect "Views (M)" slider | `transform/scale` keys: 0 s 195.81 % (out: speed −425 %/s, influence 1.97 %) → 2.1667 s 104.074 % (in: −0.4625 %/s @ 95.12 %; out: −0.4625 %/s @ 5 %) → 4.2333 s 100 % (in: −5.5 %/s @ 26.28 %). The matching speeds at 2.1667 s make the hand-off seamless. `effects/#1/slider` (Views (M)): 0 s 6.8 (out: speed 220/s @ 1 %) → 1.9333 s 42.8 (in: 0 @ 95 %). |
| **Defocus** | Defocus (adjustment solid, top, not parented) | Gaussian Blur, Repeat Edge Pixels on | `effects/#1/blurriness` 40 → 0 over 0–0.3 s (out −130/s @ 33 %, in −110/s @ 33 %): blurs every layer below it. |
| **Trend arrow** | Arrow (shape) | ↗ drawn as two open paths (shaft (−22, 21.5)→(21, −21.5); head (−6, −21.5)→(21, −21.5)→(21, 5.5)), stroke `#5ceb45` 6.5 px, round cap + join. Deep Glow: Radius 150, Exposure 0.02, Spread 33, Downsample 80 (rest default). CC Light Sweep: center (960, 409.88), shape Smooth, width 50, sweep intensity 50, edge intensity 100, edge thickness 1, white, Add. | Position (−82, 53.5), static. Light Sweep **direction = `wiggle(1,100)`**: the sweep angle swings randomly about once a second by up to ±100° around −1899.7°, a living shimmer on the arrow. |
| **Counter** | Counter (text) | SF Pro Display Regular 69 px, default white fill | Position (−38, 68). Source Text expression: *read CAM CTRL's "Views (M)" slider, show it with 1 decimal, add "M"*. |
| **Views label** | Views Label (text) | "views in the last 30 days", SF Pro Display Regular 69, `#42454d`, Gaussian blur 1.5 | Position expression: *x = Counter's right edge (its position + text box left + width) + 15 px; y stays 68*. So it slides right as the number gets wider. |
| **Title** | Title (text) | "Professional dashboard", SF Pro Display Medium 86, `#454950`, Gaussian blur 2.5 | Static at (−140, −29). |
| **Card** | Card (shape) | Rounded rect 1512×345, roundness 24; vertical linear gradient (y −162.5 → 172.5): `#15171b` 0 → `#22262b` 0.36 → `#272b30` 0.63 → `#24282d` 0.9 → `#202428` 1. No stroke. | Static at (534, −7.5); runs off the right edge on purpose. |
| **Story highlights** (blurred app UI) | Highlights (shape) | 3 circles Ø296 with 10 px stroke `#1a1c21` and a vertical gradient `#8a8a8b` → `#3a3a3b` (0.45) → `#0d0d0d` (y −148 → 142), at x −20 / 350 / 720, y 358; opacities 100 / 90 / 82. Glyphs on top, fill `#080808` @ 70 %: rounded square 70×64 r8, ellipse 46×88 rotated 45°, rounded square. Gaussian blur 9. | Static. |
| **Header placeholder** (blurred app UI) | Header Placeholder (shape) | Skeleton header: icon 70×62 r12 `#121a1a` at (−230, −472); bar 1150×56 r14 `#080809` at (405, −470); avatar Ø64 `#0a0a0b` at (−225, −355); bar 1100×46 r12 `#080913` at (380, −352). Gaussian blur 12. | Static. |
| **Phone edge** | Phone (shape) | Close-up of a phone's left side, all vertical gradients: Button 18×415 r8 (`#0a0b0d` → `#565b66` → `#0a0b0d`); Rail 30×1400 metallic 9-stop (`#060607`, `#121315`, `#373a40`, `#5b5e68`, `#60636e`, `#4b4e57`, `#222327`, `#0b0b0c`, `#060607`); Edge 9×1400 (`#050505` → `#4a4c52` at 0.49 → `#050505`); Screen 1900×1600 r40 (`#010101` → `#0e1013` → `#010101`). Gaussian blur 3. | Static at the rig's centre; the button/rail at x −533…−484 form the bright sliver on the left. |
| **Light falloff** | Light Falloff (solid, Multiply) | Linear Gradient Ramp white at x 1200 → `#262626` (15 %) at x 1950 | Darkens the right third of the frame (the card fades into shadow). Parented, so it scales with the shot. |
| **Background** | BG (solid) | `#020202` | — |

Depth trick: blur rises with distance from the focal number: Counter 0, Arrow 0, Views Label 1.5,
Title 2.5, Phone 3, Highlights 9, Header 12. That's what makes a flat 2D comp read as a shallow-focus
macro shot.

## 4. Knobs (template)
| # | Knob | Layer › path | Current value |
|---|---|---|---|
| 1 | Title text | Title › `text/sourceText` | "Professional dashboard" |
| 2 | Label text | Views Label › `text/sourceText` | "views in the last 30 days" |
| 3 | Count from | CAM CTRL › `effects/#1/slider` key 1 | 6.8 |
| 4 | Count to | CAM CTRL › `effects/#1/slider` key 2 | 42.8 |
| 5 | Count duration | CAM CTRL › `effects/#1/slider` key 2 time | 1.9333 s |
| 6 | Decimals + suffix | Counter › `text/sourceText` expression | `.toFixed(1) + "M"` |
| 7 | Accent / trend colour (and direction: ↗ up) | Arrow › `contents/group/contents/stroke/color` | `#5ceb45` |
| 8 | Pull-back start scale | CAM CTRL › `transform/scale` key 1 | 195.81 % |
| 9 | Pull-back timing | CAM CTRL › `transform/scale` key times | 2.1667 s (104.074 %), 4.2333 s (100 %) |
| 10 | Focus-in amount / time | Defocus › `effects/#1/blurriness` | 40 → 0 over 0.3 s |
| 11 | Card width (fit the title/label) | Card › `contents/group/contents/rect/size` | 1512×345 |
| 12 | Right-side darkness | Light Falloff › `effects/#1/endColor` | 0.15 (`#262626`) |

## 5. Distinctive parts
| Name | What it is | From | Call | Overlaps |
|---|---|---|---|---|
| `nullPullBack` | Whole scene parented to one null that scales 195.8 → 104 % on a launch-and-glide curve (1.97 % out / 95 % in), then keeps creeping to 100 % so the shot is alive at the cut | CAM CTRL `transform/scale` | `nullPullBack(comp, {at, from: 195.81, settle: 104.074, end: 100, duration: 2.1667, creep: 2.0667})` | `cameraDrift` (proposals.json) is the slow push; this is the fast pull-back that hands off into it |
| `defocusIn` | Adjustment-layer blur 40 → 0 in 0.3 s, edge pixels repeated: the shot "racks" into focus | Defocus | `defocusIn(comp, {at, amount: 40, duration: 0.3})` | none |
| `countUp` | Text driven by a keyed slider: `toFixed(decimals) + suffix`, launch-and-glide easing | CAM CTRL slider + Counter | `countUp(textLayer, {from: 6.8, to: 42.8, at, duration: 1.9333, decimals: 1, suffix: "M"})` | same id as proposals.json `countUp` |
| `trailingLabel` | A label that stays a fixed gap right of a changing text (sourceRectAtTime + 15 px) | Views Label position expression | `trailingLabel(label, anchorText, {gap: 15})` | none |
| `trendArrow` | Green ↗ stroke arrow (round caps) with Deep Glow + a shimmering light sweep, sitting before a number | Arrow | `trendArrow(comp, {x, y, size: 43, color: "#5ceb45", direction: "up"})` | uses `accentGlow` + `lightSweep` |
| `lightSweep` | CC Light Sweep on an accent; here the angle is `wiggle(1,100)`, a continuous shimmer | Arrow `effects/#2` | `lightSweep(layer, {mode: "shimmer", wiggle: [1, 100], width: 50, sweep: 50, edge: 100})` | same id as proposals.json `lightSweep` (DJ4 uses the keyed "pass" variant) |
| `accentGlow` | Deep Glow Radius 150, Exposure 0.02 on the accent | Arrow `effects/#1` | `glow(layer, {radius: 150, exposure: 0.02})` | same id as proposals.json `accentGlow` |
| `statCard` | Dark rounded card (5-stop vertical gradient), soft grey title, sharp white number + trailing soft label | Card, Title, Counter, Views Label | `statCard(comp, {title, value, label, x, y})` | none (pairs with countUp, trendArrow) |
| `focusFalloffUI` | Fake app screen made of blurred skeleton shapes (header bars, story-highlight circles), blur growing with distance from the focal text | Highlights, Header Placeholder (+ blur ladder 1.5/2.5/3/9/12) | `focusFalloffUI(comp, {blur: [1.5, 2.5, 3, 9, 12]})` | none |
| `phoneEdgeCloseup` | Macro of a phone's left edge: side button, metallic rail gradient, bezel edge, dark screen | Phone | `phoneEdgeCloseup(comp, {x, y, blur: 3})` | `phoneMock` (proposals.json) is a whole phone; this is the extreme close-up |
| `sideFalloff` | Multiply solid with a linear ramp white → 15 % grey that shades one side of the frame | Light Falloff | `sideFalloff(comp, {from: [1200, 540], to: [1950, 540], darkness: 0.15})` | `background` (different job: shading on top, not a backdrop) |

## 6. Rebuild notes
- **Not exact:** Arrow's Light Sweep direction is `wiggle(1,100)`, seeded by the layer id; a rebuilt
  layer gets a new id, so the sweep angle differs (README: −1869.8° vs −1967.5° at 0.64 s). A
  primitive should key the angle (or seed it) instead.
- README says 42.7M; the recipe's slider ends at **42.8** (renders "42.8M").
- Counter has no explicit fill; it relies on the default white.
- Views Label's position depends on the Counter's rendered text width (font SF Pro Display must be
  installed; another font moves the label).
- CAM CTRL scale has z = 0 (2D null); harmless, but pass `[x, y, 100]` when setting it from JSX.
