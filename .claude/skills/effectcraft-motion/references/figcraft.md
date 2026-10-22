# FigCraft: where Elias designs the look

FigCraft is his Figma-class design app (MCP `figcraft-app`, app on 127.0.0.1:7979). He designs
static looks there; motion happens in EffectCraft. Rule: **FigCraft owns how things look, the kit
owns how they move**: never keep the same value in both.

## Moving designs to EffectCraft

- `edit.copyForEffectCraft {ids?}` → a native editable snapshot (shapes, gradients, text, images)
  that pastes into EffectCraft as real layers.
- `effectcraft.place {comp, project?, start?, end?}` shows a live EffectCraft comp as a card on the
  canvas that plays (`effectcraft.play / seek / explode / reveal`). Cards need EffectCraft running;
  otherwise they show a saved poster.
- FigCraft has no keyframes, only prototype transitions (`proto.interaction.add` with Smart
  Animate and a bezier), which don't carry over as keys.

## Facts that cost time (22 Oct, rebuilding reference cards)

- **Gradients:** linear, radial, angular, diamond. Handles `from` / `to` / `width` are in the
  node's unit box. A circular radial of radius R px at (cx, cy) on a w × h node:
  from `[cx/w, cy/h]`, to `[(cx+R)/w, cy/h]`, width `[cx/w, (cy+R)/h]`.
- **No 4-point gradient.** For a 4-Color Gradient look: a base fill + 4 stacked radial gradients
  (colour at alpha a → transparent at radius r). Solve colours by least squares (linear once the
  alphas are fixed) and the geometry by random search against the reference pixels
  (`~/Developer/lab/R1-rsi-intro-exam/figcraft/refcards/s1_refit.py`; fitted to AE's
  inverse-distance weighting, p ≈ 3).
- **Rims** that change brightness around the card: sample the reference rim by angle (24 stops)
  and use an angular-gradient stroke (inside, ~2.5 px).
- **Fonts:** SF Pro renders; text top = baseline − 0.952 × size (auto line height 1.193 em).
  Montserrat 0.97 × size, Nunito 1.01 × size. SF Pro Rounded doesn't render (thin fallback).
  SF Pro as outline text shows overlapping contours (variable font): use Gilroy ExtraBold for
  outlined words.
- **Components:** `component.addProperty` (text / instanceSwap), `instance.create`,
  `instance.setProperties`, `component.resetOverride {id, group}`.
- `image.place {path, x, y, width, height, parent, mode: "fill"}`, `text.style {id, start, end,
  textFills}` for one coloured word, `view.zoomSelection`.
- `run_script` runs the fc API as one undo step; `export {ids, path}` for PNGs to measure;
  `save_file` after every finished step.
- Files: a `.figcraft` is a zip with `document.json`. `figcraft-cli` is headless: `info`,
  `export`, `convert`, `render`, `run` (JSON command lists), `mcp`.

## Measuring a rebuild against a reference

Export both at the same scale, crop per element, compare zones (centre, near the rim, top vs
bottom, left vs right) in mean RGB and mean abs diff, plus row widths for corner radii. Exclude
areas the reference tints with an effect he didn't ask for (e.g. a text glow: measure the pill
away from the text). Target ≤ ~4/255 per zone.
