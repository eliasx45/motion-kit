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

## Layout
| File | What it is |
|---|---|
| `style.jsx` | `STYLE`: bg, orb, stroke, innerShadow, stagger, pop. The only place for look values |
| `lib/kit.jsx` | `unit`, `px`, `set(layer, path, value)`, `key(layer, path, time, value)`, `ease(layer, keys)`, `newComp(name, w, h, dur)`, `newShape(params)` |
| `lib/background.jsx` | `background(comp, {center?, edge?, name?})`: full-frame radial grey, sent to the back |
| `lib/orb.jsx` | `orb(comp, {shape: "circle"\|"rounded", size?, x?, y?, name?})`: radial gradient, inner shadow, hairline stroke |
| `lib/pop.jsx` | `pop(layer, {at?})`: scale in with one overshoot and one rebound, fading in |
| `lib/stagger.jsx` | `stagger(layers, {at?, step?, order?: "in-order"\|"reverse"\|"center-out", enter?})`: enter many layers one after another; `enter` is any entrance primitive (default `pop`) |
| `hero.jsx` | Scene: orb + rounded square, side by side (landscape) or stacked (portrait) |
| `row.jsx` | Scene: 5 orbs (alternating circle/rounded) in a row, staggered center-out |
| `hero-vertical.jsx` | `hero.jsx` at 1080×1920 (sets `SIZE` before including) |
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

## Adding a primitive
1. Write it as a function in `lib/<name>.jsx` that takes `(comp or layer, options)`, reads look
   values from `STYLE` (add knobs there), and returns the layer it made.
2. Use it in a scene at the top level (`<scene>.jsx`) and `#include` what it needs.
3. `./build.sh <scene>`, look at the render, then `--bless` to save the reference.
4. Add it to the Layout table above and to README.md. Commit the primitive, the scene and its
   reference together.

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

## Reusing finished comps
Don't screenshot a library comp and guess. Read how it's made: `effectcraft-cli props <comp>
<layer> --project F` (and `comp.motion` for timing). When EffectCraft has `comp.recipe` (being
added), use it to get a compact recipe of everything authored. Then rebuild from the kit, or
extract what's new into a primitive.
