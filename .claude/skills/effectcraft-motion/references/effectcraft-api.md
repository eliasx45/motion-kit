# EffectCraft for builders: the JSX/JSON you actually need

Full docs: `~/Developer/effectcraft/docs/agents.md` (MCP, CLI, recipes, pitfalls) and
`docs/control-protocol.md`. Find any command with `$EC commands --filter <word>` or the MCP's
`command_list {filter}`; `describe_command` gives its params and JSON Schema.

## Contents
- [Three ways in](#three-ways-in)
- [The JSX pattern](#the-jsx-pattern)
- [Times](#times)
- [Layers you'll make](#layers-youll-make)
- [Property paths](#property-paths)
- [Keys and eases](#keys-and-eases)
- [Peaks on words](#peaks-on-words)
- [Effects and styles](#effects-and-styles)
- [Recipes](#recipes)
- [Gotchas](#gotchas)

## Three ways in

| Way | When | Example |
|---|---|---|
| CLI, own project file | default for building and experiments | `nice -n 10 $EC script /abs/build.jsx --save-as /abs/out/a.ecproj` |
| CLI one-offs | inspect, render, compare | `$EC props Main '#1' --project a.ecproj`, `$EC render-frame a.ecproj --time 1 --max-side 960 --out f.png`, `$EC compare ref.png f.png --json` |
| MCP / live app | only for Elias's edit, as the agent client | `command_run`, `run_script`, `render_frames`, `get_motion`, `lint_frame` |

- `EC=~/Developer/effectcraft/scripts/fork/cli.sh` rebuilds the CLI when the code changed (the
  first call after a merge can take a minute or two). Experiments pin a copy.
- The CLI opens the demo project unless you pass a project, `--project F`, or `--empty`.
- `$EC run a.ecproj comp.open '{"comp":"Main"}' render.contactSheet '{"count":8,"path":"/abs/sheet.png"}'`
  chains commands in one headless session. `$EC render a.ecproj --comp Main --format h264 --out a.mp4`
  renders video (`--resolution half|quarter`, `--format gif --fps 12` for previews).

## The JSX pattern

JSON is the vocabulary (each step an engine command with JSON params), JSX is the grammar
(variables, maths, loops decide which commands run with which numbers):

```js
#include "kit.jsx"        // copy kit.jsx / graphs.jsx next to your script: includes are folder-local
#include "graphs.jsx"
var F = 1001 / 30000;                                         // one frame at 29.97
var c = newComp("Main", 1920, 1080, 6);                       // sets COMP, 29.97 fps
app.beginUndoGroup("build");
var ctrl = app.run("layer.newNull", { name: "B1 CTRL" }).layer;
var card = newShape({ kind: "rounded", size: [640, 360], position: [960, 600],
  roundness: 40, name: "B1 Card 0", fill: "#0e2138", strokeWidth: 0 });
var txt = app.run("layer.newText", { text: "Hello", name: "B1 Card 0 T", size: 96, fill: "#ffffff",
  position: [960, 632] }).layer;
key(card, "transform/position", 15 * F, [960, 720, 0]);       // keys in COMP space…
key(card, "transform/position", 41 * F, [960, 600, 0]);
key(card, "transform/opacity", 15 * F, 0);  key(card, "transform/opacity", 20 * F, 100);
key(txt, "transform/opacity", 15 * F, 0);   key(txt, "transform/opacity", 20 * F, 100);  // opacity isn't inherited
graph(card, "transform/position", 15 * F, 41 * F, "Quick launch · soft landing");
graph(card, "transform/opacity", 15 * F, 20 * F, "Quick launch · soft landing");
graph(txt, "transform/opacity", 15 * F, 20 * F, "Quick launch · soft landing");
app.run("comp.addMarker", { time: 15 * F, comment: "B1 · \"what these pages have in common\"" });
graphsFinish();
app.run("time.set", { time: 41 * F });                        // …then parent LAST, at a frame where
app.run("layer.setParent", { layers: [card], parent: ctrl }); // the parents are at rest: keys are
app.run("layer.setParent", { layers: [txt], parent: card });  // converted, children stay put
app.run("layer.setSwitch", { layers: [ctrl], "switch": "video", value: false });
app.endUndoGroup();
```

Tested 22 Oct (lab R2 route shoot-out, the same card built 3 ways): JSX + commands, a
hand-written recipe and After Effects object-model JSX all render pixel-identical and pass
`check_graphs.py` 5/5. Commands + `graph()` is the shortest and converts every Graph (Fast In's
speed included); the AE model works but needs real speeds by hand; recipes are best for copies.

- `app.run(id, params)` returns the command's JSON reply (`.layer`, `.uid`, `.path`, …).
- `app.project.activeItem` and the After Effects object model exist too (`comp.layers.addText`,
  `layer.property(…)`), but prefer commands: they validate and fail loudly.
- `writeLn(...)` / `$.writeln(...)` print; the last expression's value is returned.
- Scripts may read files in the project's folder only, and can't write files or use the network
  unless Elias enables it.
- Kit helpers (`~/Developer/motion-kit/lib/kit.jsx`): `unit`, `px`, `set`, `key`, `ease`,
  `newComp`, `target`, `newShape`, `get`, `velocity`. Primitives: `orb`, `rect`, `pop`,
  `slideUp`, `stagger`, `background` (their eases are the kit's generic ones: re-ease with
  `graph()`).

## Times

- Seconds everywhere. Exact time is `Tick` (254 016 000 000 / s); writes snap to comp frames.
- **Keyframe times are layer time.** `add_keyframe` / `set_property` / `prop.addKey` take layer
  time unless `timeBase: "comp"`. `get_property`, `render_preview`, `run_script`'s
  `setValueAtTime` and `keyTime` use comp time. Easiest: keep built layers starting at 0.
- 29.97 fps (his edits): frame n = n × 1001 / 30000 s. Write fractions exactly (`600 / 1080`,
  `n * 1001 / 30000`): rounding shows up in compares. A reference at 30 fps: `newComp(name, w, h,
  dur, 30)` and `F = 1 / 30`. Match the reference's fps or every frame drifts.
- Frames count from 0 everywhere in EffectCraft (`render-frame --frame 0` = time 0). Write briefs
  in 0-based frames too.
- `layer.timing {layers, start}` moves a layer in time with its in and out points.

## Layers you'll make

| Command | Key params | Reply |
|---|---|---|
| `comp.new` | `name, width, height, frameRate, duration` | `{comp}` |
| `shape.newShape` | `kind: rect\|rounded\|ellipse\|polygon\|star, size, position (centre), roundness (px), name, fill, fillType: linear\|radial, stroke, strokeWidth` | `{layer, group}` |
| `layer.addShapeItem` | `layer, kind (rect, ellipse, path, fill, stroke, gfill, gstroke, trim, repeater, round, …), group?` (pass `group: "contents/group"` to add inside a `newShape` shape; without it the item lands at the layer root) | `{uid, path}` |
| `layer.newText` | `text, name, position, box (paragraph), font, style, size, fill, tracking, leading, justify, allCaps` | `{layer}` |

`position` of point text is its baseline, **horizontally centred by default**: pass
`justify: "left"` to put the left edge there (left-aligned rows, list items).
| `layer.newSolid` | `color, name, size?` | `{layer}` |
| `layer.newNull` | `name` | `{layer}` |
| `layer.setParent` | `layers, parent (layer or null), compensate?` | |
| `layer.precompose` / `comp.fromRecipe` | | |
| `comp.addMarker` | `time, comment` | |
| `layer.addMarker` | `layers, time, comment` | |

Layer order: create the background first, or `layer.arrange {layers, to: front|forward|backward|back,
index? (1-based), above?: layer}`.

Fonts: `list_fonts` / `$EC commands --filter font` before using one; a missing font silently falls
back. Check text width in a render.

## Property paths

Paths are what `$EC props <comp> <layer> --project F` or `get_layer {flat: true}` print:
`transform/position`, `transform/scale` ([x, y, z] in %), `transform/opacity`,
`transform/rotation`, `contents/group/contents/gfill/colors`, `contents/group/contents/stroke/width`,
`layerStyles/innerShadow/size`, `effects/#1/blurriness`, `@uid` (from a reply's `uid`).
Transform: `transform/anchor` (not anchorPoint), `position`, `scale`, `rotation`, `opacity`.
A radial gradient's `start` / `end` are in the shape layer's own space: `[0, 0]` = the layer's
position (the shape's centre).

- Gradients: `set(layer, ".../gfill/colors", {colors: [[0, "#0080ff"], [1, [1, 1, 0]]], opacities: [[0, 1], [1, 1]]})`;
  `.../gfill/type` `"Radial"`, `.../gfill/start` and `/end` in layer space (radial: end − start = radius).
- Vectors: give 3-D values for transform (`[x, y, 0]`, `[100, 100, 100]`): `property("Scale").setValueAtTime(t, [x, y])` sets z to 0 on older builds.

## Keys and eases

- Add keys: `prop.addKey {layer, path, time, value}` (`key()` in kit.jsx); several at once:
  `add_keyframe {layer, path, keys: [{time, value}…]}` over MCP. `prop.set` with a time only sets
  the value of an unkeyed property; on a property that has keys it adds (or replaces) a key there.
- Keys may sit before frame 0 or after the comp's end: that's how a shot starts mid-move after a
  cut (the move's tail plays from frame 0).
- Ease a key: `keys.select {keys: [{layer, path, time}]}` then `keys.velocity {outSpeed, outInfluence}` /
  `{inSpeed, inInfluence}` (arrays per dimension; speed in value units per second; influence %).
  Or `keys.setEase {layer, path, time, side: in|out, speed, influence}` for one side of one key.
- **His Graphs:** copy [graphs.jsx](../assets/graphs.jsx) next to your script.
  `graph(layer, path, t0, t1, "Fast In")` puts a card on the move t0 → t1 (comp seconds, keys
  must exist); it converts the card's normalised speed (`speed × Δv / Δt`, position uses the path
  length, mask paths progress 0 → 1). `graphChain(layer, path, [t0, t1, t2], [name, name])` for a
  pop or punch. Run `graphsFinish()` once at the end: keys added later (an exit starting inside a
  move) split segments, so every logged move is re-applied.
- `"Expo In-Out (Elias)"` in graph() picks its influences from the move's duration.
- Spatial paths: position keys default to auto-Bezier motion paths. A straight move between two
  keys is straight; a third key bends it (that's the drift overshoot). Set linear spatial
  interpolation (`keys.interpolation`) when you need a straight multi-key path.
- `keys.copy` / `keys.paste`, `keys.quickOffset {delta}` (stagger selected layers' keys),
  `layer.quickOffset`.
- Colour: a solid fill / stroke `color` keys and eases with graph() per channel. **Gradient**
  colours (`gfill/colors`) interpolate between keys but graph() can't ease them: crossfade a lit
  copy over a dim one with opacity instead.
- **Lit ↔ dim states** (a list row taking focus): key one opacity per row on all its parts (body,
  rim, icon, text) together, 100 lit / ~34 dim, over a dark background. Moon Edits S13: dim over
  ~13 f with Smooth emphasis; a new row lights over ~26 f with Fast In. A Fill effect
  (`ec.generate.fill`) colour also works for text alone.

### Overlapping moves (R2 round 1, 22 Oct: every builder hit this)

One property holds one key chain, so two moves can't overlap on it (his overlap rule: the next
move starts at ~60 % of the previous). Put each move on its **own stacked null** and let them add
up: `CTRL` → `List A` → `List B` → `List C` → the elements. Each null gets its own Graph. Moves
that don't overlap stay one key chain.

Recipe (R2 round 2, 22 Oct: 4 of 4 builders scored at the ceiling with it). This rig is the
exception to "parent last": no frame has every null at rest, so
1. make the nulls **neutral**: a new null's anchor is `[50, 50, 0]` (it's 100 × 100), so set
   `transform/anchor` = `[0, 0, 0]` and `transform/position` = `[0, 0, 0]` on the offset nulls; the
   zoom null (`CTRL`) keeps position = its pivot (e.g. `[960, 540, 0]`) with anchor = that same
   point, so its children's coordinates stay comp coordinates;
2. build the elements and parent **everything before adding any key** (nothing moves yet, so
   parenting at any time is exact);
3. key each null as an offset from its rest value (`[0, +Δ, 0]` → `[0, 0, 0]`: ends at rest, so the
   layout you built is the final frame) and put its Graph on it.

### Matching a measured move to his Graphs

Rebuilding a reference: measure the element per frame (position, scale, opacity…), then
`python3 scripts/fit_graph.py samples.json [--moves N] [--fps 30]` names the Graph, start and end
frame and values for each move (with N > 1 the moves add up: build them as stacked nulls). It
lists the next best fits too; RMS ≤ ~1–2 px means the Graph is right.

When the automatic search lands badly (several overlapping moves, RMS ≫ 2 px):
1. `--speed` prints the per-frame speed. Each move is one hump: it starts where the speed leaves
   its low, peaks, and ends at the next low. Moves overlap when the speed never reaches 0.
2. Seed one move per hump: `--seed "Fast In:-2:30;Smooth emphasis:10:54;…"`.
3. Add `--free` to also fit **custom eases** (speed 0 at both keys, any influences). If they beat
   the Graphs clearly, the reference doesn't use his Graphs: give the custom eases (out / in
   influence) in the brief. Moon Edits S11 (22 Oct): Graphs ~8 px, custom eases 4 px.
Custom eases are for **rebuilding references** only; his own builds use his Graphs. Apply them
with `cease(layer, path, t0, t1, outInf, inInf)` from graphs.jsx and check with
`check_graphs.py --reference` (lists them apart instead of as unmatched).
With 4+ moves, seed one move per speed hump **plus a long slow "carrier"** under the steps when
the speed never settles between them (S11: 5 moves, 1.4 px; 4 moves, 4 px).

## Peaks on words

1. Speech map: `scripts/fork/speech-map MEDIA --start S --dur S --fps 29.97 --out map.json`, then
   `speech.import {path, layer?}` (layer = the voice footage, so media time maps through it).
2. `speech.get {stressed: true}` lists accents with `accentFrame` (where a peak goes).
3. `keys.alignPeak {layer, path, speech: "content" | frame | time, mode?, graph?}` moves a keyed
   move so its speed peak lands on the target (±0.5 f), one undo step. Modes: `shift` (default),
   `stretch-in`, `stretch-out`, `ease` (keys stay, influences change). `graph`: `fast-in`,
   `quick-launch`, `smooth-emphasis`, `slow-launch`, `fast-out`, `keep` or a custom
   `{out: {speed, influence}, in: {…}}`. Without it, the graph peaking where the target falls is
   picked.
4. Check: `speech.accents {layer?}` (every speed peak, nearest accent, `offsetFrames`, `hit`
   within 1 f) and `lint_frame {rules: ["off-accent"]}`.

## Effects and styles

- `effect.apply {layer, effect}` (name or id) → `{effects, paths: ["effects/#2"]}`;
  `add_effect {layer, effect, values}` over MCP; `list_effects {filter}` for param ids.
- **4-Color Gradient** `ec.generate.fourcolor`: `positionsColors/point1..4` (vec2),
  `positionsColors/color1..4`, `blend` (1–1000, default 100), `jitter`, `opacity`, `blendingMode`.
  Check the point space with `get_layer` before setting (defaults read like fractions of the layer).
- **Deep Glow (Native)** `ec.stylize.deepglow`, Glow `ec.stylize.glow`: only when he asks or the
  reference has it.
- Gradient Ramp, Drop Shadow, CC Light Sweep etc. exist under their After Effects names.
- Layer styles: `layer.style.add {style: dropShadow|innerShadow|outerGlow|innerGlow|bevelEmboss|satin|colorOverlay|gradientOverlay|stroke}`
  (or `layer.style.innerShadow` etc.), then `layerStyles/<style>/<param>`, e.g.
  `layerStyles/innerShadow/{useGlobalLight, angle, distance, size, choke, opacity, color}`,
  `layerStyles/outerGlow/{opacity, color, size, spread}`; `$EC props` lists every one.
  Style values don't carry over 1 : 1 from what you see in After Effects: measure the result. In
  R2 an Outer Glow at 25 % / size 80 gave +20–30/255 next to the rim; ~8–10 % gave a faint +8.
  Measure an effect by rendering it on and off and diffing the two.
  Outer Glow **`spread` > 0 jumps**: it grows the hard shape first, so a 45 %-opacity fill glows
  as if opaque (R2 r3: spread 0 → +65/255, spread 1 → +148). Keep spread 0 on see-through shapes.
- **Gaussian Blur:** σ (px) ≈ 0.29 × blurriness (three R2 builders measured 0.287–0.297), so a
  brief's σ 16 → blurriness 55.
- **Motion blur:** `comp.setSwitch {switch: "motionBlur", value: true}` + `layer.setSwitch
  {switch: "motionBlur"}` on the moving layers; `comp.settings {shutterAngle: 180, shutterPhase:
  -90, motionBlurSamples: 32}` (the default sample count shows ghost copies on fast moves).
- Motion Library: `library.search {query}`, `library.insert {id, time}`, `library.apply`;
  Bounce: the `toolkit_bounce` MCP tool (acts on the user's selection: only in his edit, with care).

## Recipes

Compact JSON of only what was authored: structure, changed props by path, keys with easing,
effects, styles, masks, text, precomps. Rebuilds within one 8-bit level.

```sh
$EC exec comp.recipe --params '{"comp":"Main","path":"/abs/x.recipe.json"}' F.ecproj --json
$EC run --empty file.newProject '{}' comp.fromRecipe '{"path":"/abs/x.recipe.json"}' file.save '{"path":"/abs/rebuilt.ecproj"}'
```

- Keys in a recipe: `{keys: [{time, value, in?, out?}]}`, layer time, easing `easy`, `hold`,
  `bezier` or `[[speed, influence]…]` per dimension. **Influence is a fraction** (0.3988 =
  39.88 %) and **speed is real** (value units / s, not the card's normalised speed).
- Values of a parented layer are in the **parent's space** (a child of a 100 × 100 null at the
  comp centre: comp [960, 540] → [50, 50]). Hand-writing a recipe with parents means converting.
- Comp **marker times are ticks** (0.4 s = 101 606 400 000) while key times are seconds.
- A solid's `color` must be RGB numbers (`[0.047, 0.078, 0.137]`); hex works in `props` values.
- Check `unsupported` in `comp.recipe`'s reply.
- Elias's 8 reference comps live as recipes + GIFs + breakdowns in `motion-kit/references/`.

## Gotchas

- **Parenting** (cost a round on 22 Oct): keys added *after* `layer.setParent` are in the parent's
  space, so `[960, 540]` under a CTRL null lands bottom-right. Build and key in comp space, then
  parent last. Parenting keeps each child where it is at the *current time*: `time.set` to a frame
  where the parents are at rest first, or the child lands offset (the text ended up at the card's
  top edge when parented at frame 0, while the card was still below).
- **Opacity isn't inherited** through parenting: fade children too, or precomp them.
- **Zooms and camera moves:** parent the background to the zoom null too, and make it bigger than
  the frame, or it stays still while everything else scales (R2: the reference's vignette zoomed
  with the list and made the last motion peak at the cut).
- `$EC set … --project F` changes only that process's copy: add `--save` (or `--save-as F2`), or
  do the change and the render in one `$EC run …` / script.
- `render.contactSheet` params are snake_case (`max_side`), unknown keys are rejected.
- `shape.newShape` with a shape layer selected adds into it: deselect first (`newShape()`).
- `shape.newShape` strokeWidth defaults to the Tools bar's: always pass it (0 = no stroke).
- `#include` only reaches files in the script's own folder or below; run scripts by absolute path.
- A reference to a layer name that doesn't exist is an error, never a no-op: read errors.
- A script that throws keeps the edits it made: wrap in `app.beginUndoGroup` / `endUndoGroup`.
- `run_script` stops after 300 s by default; long builds: split them or raise `timeout`.
- Headless MCP without `--autosave` keeps the project in memory: `save_project` after milestones.
- Precomp layers show nothing outside their nested comp's span.
- Expressions return `[v, v, v]` from selectors; a syntax error leaves the expression disabled
  and the value rendering (read `expressionError`).
- Motion blur, 3-D and heavy glows multiply render time: keep previews at ≤ 960 px.
