# DJ5 Card Variants: breakdown

## 1. What it is
A reel card gets a "+5% Speed" tag. Then two copies of the card are scanned with a yellow light. The right copy fails the scan: a red **DUPLICATE** stamp slams onto it and the card shakes. The camera then pans left, "Flipped" and "+5% Speed" labels appear beside the right card, and its outline turns green.
**14.57 s, 1920×1080, 30 fps.** Comp background `#030303`.

## 2. Timeline
| Time (s) | Beat |
|---|---|
| 0.00–0.03 | The whole frame starts blurred (FX blur 12→0 in one frame) |
| 0.00–4.80 | **Card 1** (centred) creeps in: scale 111.85→120.4 %, linear |
| 2.47–3.80 | **"+5% Speed" tag** appears inside the card's bottom edge and drifts up 4.6 px |
| 4.73–5.17 | **Blur-cut**: FX blur 0→12→24→14→11→0. At 4.80 Card 1 is replaced by **Card L + Card R**. **Flash** (Add, `#191919`) fades 100→0 from 4.83 to 5.27 |
| 4.83–9.20 | **CTRL rig zoom-out**: scale 136.38→99.74 %, fast start with a long glide in |
| 4.83–5.53 | Yellow **scan tint** fades in on both cards (opacity 0→100) |
| 5.33–8.20 | **Scan line** rises from the bottom (97.8 %) to the top (0 %) of both cards |
| 6.00–6.70 | Each scan's tail grows from 1 % to 50 % of the card's height (a soft yellow band below the line) |
| 7.03–7.93 | Card L's tail shrinks to 3 %, so its scan becomes a thin line at the top |
| 7.40–7.77 | Card R's scan turns yellow→orange→red, then cuts out (75 % at 7.73, 0 at 7.77) |
| 7.63–7.77 | Card L dims to 52 % |
| 7.67–7.87 | **DUPLICATE stamp** slams onto Card R: scale 240.4→100 %, opacity 0→100 in 4 frames |
| 7.70–7.80 | Card R's outline goes white→red |
| 7.83–8.13 | **Card R shakes** sideways (6 px, 6 Hz, dying out) |
| 8.27–8.73 | Card L's scan tint fades out |
| 9.40–11.37 | **CTRL pans** 262 px left, then keeps drifting another 8.3 px until the end |
| 9.43–14.57 | **CTRL slow push-in**: 99.74→104.51 %, linear |
| 9.73–9.80 | Stamp flickers out (100→20 % held, gone at 9.80) |
| 9.73–10.67 | Card L dims further, 52→25 % |
| 9.97–11.13 | **"Flipped" label** (with flip icon) appears right of Card R and rises 8.2 px |
| 11.27–12.60 | **"+5% Speed" label** (with fast-forward icon) appears below it and rises 10 px |
| 13.63–13.77 | Card R's outline turns green, flickers orange for one frame, then green again |
| 14.50–14.53 | Blur out at the end (FX blur 0→12) |

## 3. Elements
Colours as hex. "infl" = influence %. A speed of 0 is a flat ease. Keyframes with no easing listed are linear.

### Stage
| Layers | Look | Motion |
|---|---|---|
| `DJ5 Card Variants - BG` (solid) | Gradient Ramp, Radial: start [960, 540] `#090909` → end [2110, 540] `#020202`, **Scatter 50** | none |
| `DJ5 Card Variants - FX` (adjustment solid, top) | Gaussian Blur + **Deep Glow over everything**: Radius 150, Exposure 0.02, Spread 33, Downsample 80, Threshold 0, Screen, Dither on | `effects/#1/blurriness` keys (below) |
| `DJ5 Card Variants - Flash` (solid `#191919`, **Add**, in 4.80 / out 5.30) | adds a grey lift to the whole frame | `transform/opacity` 100 @4.83 → 0 @5.27, linear |

FX blur keys: 0 s **12** → 0.033 **0** … 4.733 **0** → 4.767 **12** → 4.8 **24** → 4.867 **14** → 5.0 **11** (in speed −22.5, infl 33.3; out speed 0, infl 30) → 5.167 **0** (in infl 60, out easy) … 14.5 **0** → 14.533 **12**.

### Reel card (Card 1, Card L, Card R: same art)
Shape layer with 4 groups, all 360 × 588.5 at roundness 26:
- **Fill**: rect `#1a1a21`.
- **Card**: rect + **Border** stroke, white, 2.5 px. Plus a **Tint** gradient fill (`gfill`) for the scan.
- **Play**: ellipse 84 × 84 with a white stroke, 3 px, 35 % opacity.
- **Triangle**: 3-point polygon, radius 20, rotation 90, at [−2, 0], white fill at 45 %.

| Card | Where | Motion |
|---|---|---|
| `Card 1` (0–4.80) | [959.5, 540.87], no parent | `transform/scale` 111.85→120.4 %, 0→4.8 s, linear. Its Tint is at 0 % (unused) |
| `Card L` (4.80→) | parent CTRL, [−202.5, 0] | `transform/opacity`: 100 @7.633 → 52 @7.767 (in speed −360 %/s, infl 33.3; out easy) → hold to 9.733 (in easy, out infl 15) → 25 @10.667 (in infl 85) |
| `Card R` (4.80→) | parent CTRL, [202.5, 0] (45 px gap between the cards) | Border colour: white @7.7 → `#ed0f14` @7.8 (linear, then hold) → `#3ded45` @13.633 → `#b84c2e` @13.7 → `#3ded45` @13.767 (all held). **Shake expression** on position |

**Shake expression** (Card R `transform/position`): from frame 235 (7.833 s), for 0.3 s, it adds `6·sin(2π·6·u)·(1−u/0.3)` px to x. In words: a 6 px, 6 Hz sideways wobble that dies out in a straight line over 0.3 s.

### Scan (the yellow light that sweeps up the cards)
The scan is each card's `Tint` gradient fill, driven by three sliders on `CTRL`:
- **Gradient**: linear, colour `#fcdb00` all along. The opacity stops are 0 % at 0, 100 % at 0.01, 100 % at 0.35 and 0 % at 1. So there is a hard top edge, a solid band, then a fade downwards.
- **Start Point expression**: `[0, −294.25 + 588.5·ScanTop]`. The scan line sits at that fraction of the card's height (0 = top edge, 1 = bottom edge).
- **End Point expression**: `[0, −294.25 + 588.5·(ScanTop + Tail)]`. The tail is the length of the band, as a fraction of the card's height. Card L uses Tail L, Card R uses Tail R.

| Slider (CTRL) | Keys |
|---|---|
| `Scan Top` | 0.978 @5.333 (out infl 57.9) → 0 @8.2 (in infl 73.8). An S-curve rise over 2.87 s |
| `Tail L` | 0.01 @6.0 (out infl 15.2) → 0.5 @6.7 (in 13.6, out 33) → 0.5 @7.033 (in easy, out 1) → 0.03 @7.933 (in 42.6) |
| `Tail R` | 0.01 @6.0 (out 15.2) → 0.5 @6.7 (in 13.6, out 33) → 0.53 @7.467 (in 60) |

Tint opacity, both cards: 0 @4.833 (out infl 20) → 100 @5.533 (in infl 70).
- Card L: holds to 8.267, then 100→0 by 8.733, leaving and arriving at −214 %/s with infl 33.3.
- Card R: 100 @7.7 → 75 @7.733 (held) → 0 @7.767 (held).

Card R's tint colour keys (linear, every 2 frames): `#fcdb00` @7.4 → `#fdc100` @7.467 → `#fd6000` @7.533 → `#fd0300` @7.6 → `#fb0c0b` @7.667 → `#ff3531` @7.733.

### DUPLICATE stamp
| Layers | Look | Motion |
|---|---|---|
| `Stamp` (shape, parent Card R, 7.667–9.80) at [−2, 3], rotation **−14.7°** | Outer: rect 404 × 108, roundness 10, stroke `#ed0f14` 8 px. Inner: rect 384 × 88, roundness 5, stroke `#ed0f14` 3 px, fill `#660508` at 45 % | **Scale** 240.4 @7.667 (out speed 0, infl 21.4) → 100 @7.867 (in speed −156 %/s, infl 100). It is still moving when it lands, so it thuds. **Opacity** 0 @7.667 → 30 @7.733 → 50 @7.767 → 100 @7.8 (linear) … held 100 @9.733 → 20 @9.767 (held), and the layer ends at 9.80 |
| `Stamp Text` (parent Stamp) at [−0.92, 29.53], scale [100, 96.31] | "DUPLICATE", Impact 82, tracking 10, centred, `#ed0f14` | Opacity expression `thisComp.layer("Stamp").transform.opacity` (follows the stamp) |

### Labels and icons
All text is SF Pro Display Medium, white. Icon blue: `#0b93f9`.

| Layers | Look | Motion |
|---|---|---|
| `Tag Speed` (parent Card 1, 2.467–4.80) + `Tag Icon` | "+5% Speed", 36 px. The icon is two 3-point polygons (radius 14.7, roundness 20, rotation 90, at ±10.5), group scale [70, 100], at [−34, −10.5] from the text | Position [−65, 262.2] → [−65, 257.6] from 2.467 to 3.8. Out speed 60 px/s, infl 10; in infl 80 |
| `Label Flipped` (parent CTRL, 9.967→) + `Icon Flipped` | "Flipped", 42 px. The **flip icon** is two polygons pointing away from each other (radius 13.3, roundness 15, rotations 90 and −90, at ±17), group scale [88, 100], plus a dashed vertical line (a Repeater: 5 copies of a 4 × 6.5 rect at roundness 2, 10 px apart). Icon at [−42.3, −11.2] | Position [491, −25.3] → [491, −33.5] from 9.967 to 11.133. Out speed 40, infl 12; in infl 80 |
| `Label Speed` (parent CTRL, 11.267→) + `Icon Speed` | "+5% Speed", 42 px. **Fast-forward icon**: polygons radius 16.7, roundness 20, rotation 90, at ±12, group scale [80, 100]. Icon at [−41.1, −12] | Position [486, 46.5] → [486, 36.5] from 11.267 to 12.6. Out speed 40, infl 12; in infl 80 |

The labels have no fade: each one appears on its in-point and drifts up a few pixels.

### CTRL rig (null, 4.80→)
Card L, Card R and both labels are parented to it. Anchor [0, 0].
- **Scale**: 136.38 @4.833 (out speed 0, infl 0.1) → 99.74 @9.2 (in infl 95.6) → hold → 99.74 @9.433 → 104.51 @14.567 (linear).
  - An almost-zero out influence plus a 95.6 % in influence gives an extreme expo-out: it snaps most of the way at once, then glides for 4 s.
- **Position**: [960, 539.5] @9.4 (out infl 37.7) → [697.93, 539.5] @11.367 (in speed 2.57 px/s, infl 100) → [689.67, 539.5] @14.567 (out/in speed 2.57, infl 0.1).
  - In words: an ease-out pan that arrives at exactly the speed of the drift that follows, so it hands over to a constant 2.57 px/s drift with no stop.

## 4. Knobs (if this were a template)
| Knob | Layer · path | Current |
|---|---|---|
| Tag text (on the single card) | `Tag Speed` · Source Text | "+5% Speed" |
| Variant label 1 | `Label Flipped` · Source Text | "Flipped" |
| Variant label 1 icon | `Icon Flipped` (shape) | flip glyph |
| Variant label 2 | `Label Speed` · Source Text | "+5% Speed" |
| Variant label 2 icon | `Icon Speed` (shape) | fast-forward glyph |
| Stamp word | `Stamp Text` · Source Text | "DUPLICATE" |
| Stamp / fail colour | `Stamp` strokes, `Stamp Text` fill, `Card R` border key @7.8 | `#ed0f14` (stamp fill `#660508` at 45 %) |
| Pass colour | `Card R` · `contents/group/contents/stroke/color` keys @13.633 and @13.767 | `#3ded45` (flicker `#b84c2e`) |
| Scan colour | `Card L` / `Card R` · `contents/group/contents/gfill/colors` | `#fcdb00` (R ramps to red) |
| Icon colour | `Icon*` / `Tag Icon` · `contents/group/contents/fill/color` | `#0b93f9` |
| Card art / thumbnail | the cards' `Fill` group (could hold footage) | flat `#1a1a21` with a play button |
| Card size | `contents/group*/contents/rect/size` | 360 × 588.5, roundness 26 |
| Stamp angle | `Stamp` · `transform/rotation` | −14.7° |
| Which card fails | the stamp's parent, the shake and the red/green keys on `Card R` | right card |
| Beat times | cut 4.8, scan 5.33–8.2, stamp 7.667, pan 9.4, label 1 9.967, label 2 11.267, pass 13.633 | — |
| BG colours | `BG` · `effects/#1/startColor`, `endColor` | `#090909` → `#020202` |
| Glow | `FX` · Deep Glow Radius / Exposure | 150 / 0.02 |

That is 16 knobs.

## 5. Distinctive parts
The whole comp is proposed as the template `cardVariantsVerdict` (see `dj5-card-variants.proposals.json`).

| Name | What it is | From | Call | Kit overlap |
|---|---|---|---|---|
| `reelCard` | A dark rounded 9:14.7 card with a white hairline border and a faint play button | Card 1 / L / R shape groups | `reelCard(comp, {x, y, width, play: true, fill})` | `orb` (another shape look); new look |
| `blurCut` | A hard cut hidden by a blur spike (0→12→24→14→11→0 in 0.43 s) plus an Add flash `#191919` fading over 0.43 s | FX blur keys, Flash solid | `blurCut(comp, {at, peak: 24, flash: "#191919"})` | DJ3's `defocusIn` (a blur-in only). DJ5 also opens with a one-frame blur 12→0 and closes with 0→12 |
| `scanFill` | A coloured band rising up a card, with a hard top edge and a soft tail, driven by Scan Top and Tail sliders. It can change colour as it goes (yellow→red = fail) | Tint gradients + CTRL Scan Top / Tail sliders | `scanFill(cardLayer, {at, duration, color, tail, failTo?})` | none (closest: `lightSweep`, which is a CC Light Sweep, not a fill) |
| `stampSlam` | A rotated double-border rubber stamp with a word, dropping from 240 % to 100 % in 0.2 s and landing with speed, flickering out | Stamp + Stamp Text | `stampSlam(layer, {text, color, at, hold, angle: -14.7})` | `pop` (scale entrance, but pop overshoots; this slams down from big) |
| `impactShake` | A decaying sine shake: 6 px, 6 Hz, 0.3 s, along x | Card R position expression | `impactShake(layer, {at, amplitude: 6, freq: 6, duration: 0.3, axis: "x"})` | none |
| `outlineVerdict` | A card's outline changing to a status colour: white→red over 0.1 s (fail), later held green with a one-frame orange flicker (pass) | Card R border colour keys | `outlineVerdict(layer, {at, color, flicker?})` | none |
| `dimAway` | A losing option fading back in two steps: 100→52 % fast, then 52→25 % slowly | Card L opacity | `dimAway(layer, {at, to: [52, 25], second})` | DJ1's `focusBranch` lights the winner; this dims the loser (could be its option) |
| `featureLabel` | An icon + label line (SF Pro Medium 42, blue icon) beside a card, appearing with a small upward settle | Label/Icon Flipped, Label/Icon Speed, Tag Speed/Icon | `featureLabel(comp, {text, icon: "speed"\|"flip", at, x, y, parent})` | none (uses `nudgeUp`) |
| `nudgeUp` | Appears on its in-point with no fade and drifts up 5–10 px: it starts at speed (out 40–60 px/s, infl 10–12) and glides 80 % in | label/tag position keys | `nudgeUp(layer, {at, distance: 10, duration: 1.33})` | `slideUp` (same idea but tiny, no fade, starts at speed) — could be a `slideUp` option |
| `glyphIcons` | Code-drawn fast-forward and flip glyphs (rounded polygons + dashed repeater line) | Icon Speed, Icon Flipped, Tag Icon | `glyphIcon(comp, {kind: "fastForward"\|"flip", color, size})` | none |
| `nullPullBack` (same id as DJ3) | The CTRL rig: a pull-back 136.38→99.74 % (out infl 0.1, in infl 95.6) over 4.37 s, then a linear creep 99.74→104.51 %. DJ5 adds a **pan that hands over to a constant drift**: 262 px left with in speed 2.57 px/s, the same speed as the drift after it | CTRL scale + position | `nullPullBack(comp, {at, from: 136.38, settle: 99.74, end: 104.51, duration: 4.37, pan: -262.07})` | DJ3's `nullPullBack`; `cameraDrift` (the slow push. Card 1's linear 111.85→120.4 % push is that) |
| `accentGlow` (existing id) | Deep Glow Radius 150, Exposure 0.02, here on an adjustment layer over the whole comp | FX | `glow(layer, {radius: 150, exposure: 0.02})` | the existing proposal |
| `darkStage` (existing id) | Radial ramp `#090909`→`#020202`, Scatter 50 | BG | `background(comp, {look: "stage"})` | the existing proposal |

## 6. Rebuild notes
- **Scatter 50** on the BG ramp is seeded per layer, so a rebuild differs by ±2/255 (README: not exact, visually identical).
- The scan depends on **expressions that read `CTRL` slider names** ("Scan Top", "Tail L", "Tail R"). Renaming the null or the sliders breaks it quietly.
- The **shake time is hard-coded** as frame 235 (`framesToTime(235)`). If you move the stamp, update it, or key the shake instead.
- `Stamp Text` opacity follows `Stamp` by name.
- Fonts: SF Pro Display Medium and Impact must be installed, or text falls back.
- Card 1's Tint gradient exists at 0 % opacity and does nothing.
