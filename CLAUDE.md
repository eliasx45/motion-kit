# motion-kit — instructions for agents

This is Elias's motion design kit for EffectCraft: one style file, small JSX primitives, and
scenes built from them. The goal is heavily animated YouTube/explainer editing, automated with
AI. **Build from this kit; don't design from scratch.**

## How to work here
1. **Kit first.** Build every request from the primitives below. Only invent a new look or
   motion when nothing fits. When you do, say so, show it, and ask whether it should become a
   primitive.
2. **Looks live in `style.jsx`.** Never hard-code a colour, size or timing in a primitive or
   scene. Read it from `STYLE`, or add a named knob there. One-off tweaks for a single video go
   in that scene, not in `style.jsx`.
3. **Proportional, not pixels.** Sizes are fractions of the comp's shorter side (`unit(comp)`)
   or of the shape; `px(comp, v)` converts "v px at 1080p". Times are in seconds. Write fractions
   exactly (`600 / 1080`, not `0.556`): half a pixel shows up in the reference compare.
4. **Look before you say done.** Build with `./build.sh <scene>`, which renders a frame at 1 s
   and compares it with `refs/`. Open the PNG and look at it. For motion, also render a contact
   sheet (`effectcraft-cli run out/<scene>.ecproj comp.open '{"comp":"Main"}'
   render.contactSheet '{"count":8,"path":"…"}'`) or the video (`effectcraft-cli render … --format
   h264`). A deliberate look change is accepted with `./build.sh <scene> --bless`; an unexpected
   FAIL is a bug.
5. **Teach as you go.** Elias is learning JSON/JSX to automate his editing. Explain what you
   changed and why in plain words, point out reusable patterns, and say when there's a
   higher-leverage way to do something.

## Which EffectCraft
Always run EffectCraft through the fork's `scripts/fork/cli.sh` (in the EffectCraft checkout),
never a copied `effectcraft-cli`: it rebuilds the CLI first when the code changed, so you always
run the current version (`comp.recipe` and the script fixes need EffectCraft from 21 Oct 2026 on).

```sh
export EFFECTCRAFT_CLI=/path/to/effectcraft/scripts/fork/cli.sh   # build.sh and the commands below use it
```

The first run after a merge builds for a minute or two (shared with the Dock app's build); after
that it's instant. In the examples below, `effectcraft-cli` means `$EFFECTCRAFT_CLI`.

## Using the kit in a live edit
Scenes build with `target()`: with a comp open in EffectCraft, they go **into that comp at the
playhead** (no background, existing layers untouched); with nothing open, they make a new comp.
Run a scene against the running app (control port 9877, or `EFFECTCRAFT_CONTROL_PORT`):

```sh
effectcraft-cli script /abs/path/motion-kit/row-slide.jsx --bridge 9877
```

Elias is often on a deadline. Then the edit comes first: use what the kit has, make anything
missing directly in the edit, and capture it in `inbox/` (recipe + one line in `inbox/NOTES.md`)
instead of building a primitive. Turn inbox items into primitives when asked, not mid-edit.

## Layout
| File | What it is |
|---|---|
| `style.jsx` | `STYLE`: bg, orb, stroke, innerShadow, stagger, slide, pop. The only place for look values |
| `lib/kit.jsx` | `unit`, `px`, `set(layer, path, value)`, `key(layer, path, time, value)`, `ease(layer, keys)`, `newComp(name, w, h, dur)` (also sets `COMP`), `target(name, w, h, dur)` (the open comp at the playhead, or a new comp: `{isNew, t}`), `newShape(params)`, `get(layer, path, time?)`, `velocity(layer, path, time, {inSpeed, inInfluence, outSpeed, outInfluence})` |
| `lib/background.jsx` | `background(comp, {center?, edge?, name?})`: full-frame radial grey, sent to the back |
| `lib/orb.jsx` | `orb(comp, {shape: "circle"\|"rounded", size?, x?, y?, name?})`: radial gradient, inner shadow, hairline stroke |
| `lib/pop.jsx` | `pop(layer, {at?})`: scale in with one overshoot and one rebound, fading in |
| `lib/slide.jsx` | `slideUp(layer, {at?, duration?, distance?})`: rise into place on an expo-out curve (out influence 0, in influence 100), fading in; ends where the layer is |
| `lib/stagger.jsx` | `stagger(layers, {at?, step?, order?: "in-order"\|"reverse"\|"center-out", enter?, total?, duration?})`: enter many layers one after another; `enter` is any entrance primitive (default `pop`); `total` + `duration` fit the whole stagger into `total` seconds |
| `hero.jsx` | Scene: orb + rounded square, side by side (landscape) or stacked (portrait) |
| `row.jsx` | Scene: 5 orbs (alternating circle/rounded) in a row, staggered center-out |
| `row-slide.jsx` | Scene: the row rising in left to right with `slideUp`, all landed by 1.5 s |
| `hero-vertical.jsx` | `hero.jsx` at 1080×1920 (sets `SIZE` before including) |
| `inbox/` | Candidates captured during edits (recipes + `NOTES.md`), to become primitives later |
| `catalog.json` | The list of primitives and scenes `catalog.py` shows (with what each does and its call) |
| `proposals.json` | Primitives agents suggest, waiting for Elias's yes/no |
| `references/` | Elias's important comps as recipes + GIFs |
| `catalog.py` | Regenerates `catalog/`, `CATALOG.md` and `library.json` |
| `refs/` | Reference frames (`<scene>-1s.png`) that `build.sh` compares against |
| `build.sh` | `./build.sh <scene> [--bless]`; `EFFECTCRAFT_CLI` picks the CLI |

## JSON and JSX: the pattern
- **JSON is the vocabulary.** Each step is an EffectCraft engine command with JSON params,
  called from JSX as `app.run("command.id", {…})`. List commands with
  `effectcraft-cli commands --filter <word>`; `command.describe` gives one command's params.
- **JSX is the grammar.** Variables, maths, loops and `if` choose the commands and the numbers.
- Prefer `app.run` with engine commands over the After Effects object model
  (`layer.property(…)`). Commands validate their params and fail loudly; the object model can
  fail silently.
- Property paths are the ones `effectcraft-cli props <comp> <layer> --project F` prints, e.g.
  `contents/group/contents/gfill/colors`, `layerStyles/innerShadow/size`, `transform/scale`.

## The catalog: what exists, what's proposed
[`CATALOG.md`](CATALOG.md) is Elias's view of the kit: every primitive and scene with a GIF, the
open proposals, the inbox and the converted references. It's generated; never edit it by hand.

- `python3 catalog.py` rebuilds every scene into `catalog/` (project, PNG, GIF, MP4) and writes
  `CATALOG.md` and `library.json`; `--no-render` only rewrites the two files.
- `library.json` makes the kit an EffectCraft folder library: `library.addFolder {path: <kit>}`
  once, and the scenes appear in the Motion Library panel and in `library.search`.
- **Nothing is added until it's in the catalog.** After any change to a primitive or scene, run
  `catalog.py` and commit `catalog/`, `CATALOG.md` and `library.json` with it.

## Proposals: suggest, don't build
Never build a new primitive on your own. Propose it (in `proposals.json`, or per comp in
`references/<slug>.proposals.json`) and let Elias decide. `kind` is `template` (a whole comp with
knobs), `part` (one distinctive move or element) or omitted (a pattern across comps):

```json
{"id": "cardRow", "title": "2:3 post cards rising in a row", "status": "proposed",
 "why": "what it captures, in one line", "call": "cardRow(comp, {count, at})",
 "overlaps": "slideUp + stagger (would add the card look only)",
 "from": ["inbox/2026-10-21-card-row.recipe.json"], "gif": "inbox/2026-10-21-card-row.gif"}
```

`from` lists every inbox item or reference it comes from. Preview GIFs: quarter resolution at 12 fps
(`render … --format gif --resolution quarter --fps 12`), a few seconds at most. Run
`catalog.py --no-render` so it shows under **Proposed**. Elias answers yes / no / merge with
`<primitive>`; set `status` to `approved`, `rejected` or `merged` (with a `note`). Prefer extending
an existing primitive (a new option or STYLE knob) over adding a near-duplicate.

## Building an approved primitive
1. Write it as a function in `lib/<name>.jsx` that takes `(comp or layer, options)`, reads look
   values from `STYLE` (add knobs there), and returns the layer it made.
2. Use it in a scene at the top level (`<scene>.jsx`) and `#include` what it needs. When it
   comes from an inbox or reference recipe, the scene must rebuild that original:
   `./build.sh <scene>` against a reference frame rendered from the recipe.
3. `./build.sh <scene>`, look at the render, then `--bless` to save the reference.
4. Add it to `catalog.json` (and the Layout table above), run `python3 catalog.py`, commit
   everything together.

## References: Elias's converted comps
`references/<slug>.recipe.json` (+ `.gif`, and a row in `references/README.md` with the rebuild
check) are his important finished comps as recipes. **He considers them perfect as a whole.**
Take each one apart, don't boil them down to what they have in common:

- `references/<slug>.breakdown.md`: what it is, the timeline (beats with times), each element
  (its layers, look and moves with exact easing), its **knobs** (what changes per video, with
  layer + property path), its **distinctive parts**, and rebuild notes.
- `references/<slug>.proposals.json`: one `"kind": "template"` proposal (the whole comp as a
  call with knobs) and one `"kind": "part"` proposal per distinctive move or element, **even if
  it appears in only this comp**. The test is "would he reuse it on its own", not "does it repeat".
  `catalog.py` merges these files with `proposals.json` (same id = one proposal, sources merged)
  and shows templates and parts separately. Decisions go in `proposals.json` (status, note).

## EffectCraft gotchas
- `shape.newShape` adds the shape *into* the selected shape layer. Use `newShape()`, which
  clears the selection first.
- `prop.set` with a `time` doesn't create a keyframe. Use `key()` (`prop.addKey`).
- Scripts must run by **absolute path** and may only `#include` files in their own folder (or
  subfolders), so scenes live at the top level, never in a subfolder.
- Keyframe times passed to `prop.addKey` are layer time. Keep layers starting at 0, or convert.
- Older EffectCraft builds: in scripts, `layer.property("Position")` on a shape layer could hit
  the shape group's Position, and `property("Scale").setValue([x, y])` set z to 0. Use
  `app.run("prop.set", …)` with full `[x, y, 100]` values to avoid both.

## Reusing finished comps (recipes)
Never screenshot a library comp and guess. Read how it's made with a **recipe**: compact JSON of
only what was authored (structure, changed property values by path, keyframes with easing,
styles, effects, masks, text, precomps).

```sh
effectcraft-cli exec comp.recipe --params '{"comp":"Main","path":"/abs/x.recipe.json"}' F.ecproj --json
effectcraft-cli run file.newProject '{}' comp.fromRecipe '{"path":"/abs/x.recipe.json"}' file.save '{"path":"/abs/rebuilt.ecproj"}'
```

- `comp.recipe {comp?, layers?, path?}` reads a comp (`layers` picks some); its `unsupported` list
  names anything it couldn't capture. Check it.
- `comp.fromRecipe {recipe | path, name?}` builds a comp from a recipe in one undo step. Recipes
  can be edited or written by hand (hex colours are fine).
- For a Motion Library card: `library.apply` it (or open its project), then `comp.recipe` the comp.
- To turn a recipe into kit material: copy its values into `style.jsx` knobs and its structure into
  a primitive, then prove the primitive by rebuilding the original (`./build.sh`, compare).
- Needs EffectCraft `main` from 41985bc on (21 Oct 2026).
