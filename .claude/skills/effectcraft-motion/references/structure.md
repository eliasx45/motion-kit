# Structure: build it so Elias can keep editing by hand

Two sources: Elias's own comps (e.g. 10-10 Edit, comp "S2 06 Wall") and Matt's AI-to-AE harness
(`~/Developer/lab/cutsom-harness-experiment`: "fully editable comps, layers named by beat, nulls
parented, comp markers BEAT 1: …"). A rebuild that looks right but is one baked mess fails him.

## Names

| What | Pattern | His example |
|---|---|---|
| Scene comp | `<scene> <nn> <name>` | `S2 06 Wall` |
| Element | `<scene> <short> <element> <n>` (n from 0) | `S2 W Tag 0`, `S2 Wall Row 3` |
| Text layer | element name + ` T` | `S2 W Tag 0 T` |
| Controller null | `<scene> <short> CTRL`, hidden (video off) | `S2 W CTRL` |
| Background, haze | `<scene> <nn> BG`, `<scene> <nn> Haze` | `S2 06 BG` |
| Mattes | `<scene> <what> Matte`, hidden | `S2 Scan Matte` |
| Placeholders | `PLACEHOLDER <what>` | |
| Audio guide | `AUDIO <what> (Claude)`, hidden | `AUDIO sync MAIN (Claude)` |

In a fresh rebuild without a scene id, use `B1`, `B2`… (the beat) as the prefix: `B1 Card 0`,
`B1 Card 0 T`, `B1 CTRL`.

## Hierarchy

- One CTRL null per scene, parenting every moving element (rows, cards, tags). Moving or scaling
  the whole scene = one layer.
- Text parented to its card/pill, the pill to its card or precomp, the card to CTRL
  (`Tag 0 T → Tag 0 → Viral 0 → CTRL`).
- Repeated items = one master precomp, duplicated (`S2 Wall Row 0…10`). Change the master, all
  follow.
- Knobs he will touch go on the CTRL null as Effect Controls sliders with units in the name:
  `Travel Distance (px)`, `Delay (f)`, `Accent Colour`. Same names across scenes (the preset
  skill's rule).

## Beats and markers

- A comp marker at each beat's start: `B1 · "the words said"` (time = the word's frame).
- Layer markers `In` / `Out` on elements whose timing is driven by markers (presets).
- Keep the keys that are locked to a word exactly on that word's frame; the marker shows which
  word.

## Order

Top to bottom: flashes/adjustments, text, foreground elements, cards, mattes (above what they
matte), background elements, CTRL null, BG, audio guide. Layer order = depth on screen.

## Don't

- Bake motion into per-frame keys (rebuilds from a clip tend to: fit 2–4 bezier keys instead).
- Put everything in one precomp he can't open usefully.
- Leave default names (`Shape Layer 7`, `Null 2`).
- Touch his layers, selection or saved project while building in his edit.
