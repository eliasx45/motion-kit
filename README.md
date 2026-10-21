# motion-kit

**Browse it: [CATALOG.md](CATALOG.md)** (every primitive and scene with a preview, proposals, inbox).

Reusable motion for EffectCraft: one style file, small primitives, and scenes built from them.
The scripts are the source of truth; a comp is just their output.

```
style.jsx            the look: colours, sizes (as fractions), timing. Change it here, everything follows.
lib/kit.jsx          helpers over app.run (EffectCraft engine commands with JSON params)
lib/background.jsx   background(comp)                       radial grey, full frame, at the back
lib/orb.jsx          orb(comp, {shape, size, x, y, name})   radial gradient, inner shadow, hairline stroke
lib/pop.jsx          pop(layer, {at})                       scale in with one overshoot and one rebound
lib/slide.jsx        slideUp(layer, {at, duration, distance})  rise into place, expo out
lib/stagger.jsx      stagger(layers, {at, step, order, enter, total, duration})  many entrances in rhythm (any entrance primitive)
hero.jsx             scene: orb + rounded square (side by side, or stacked when portrait)
row.jsx              scene: 5 orbs in a row, rippling in from the centre
row-slide.jsx        scene: the row rising in left to right, landed by 1.5 s
hero-vertical.jsx    the same scene at 1080x1920
refs/                reference renders (frame at 1 s) that build.sh compares against
```

## Build a scene

```sh
EFFECTCRAFT_CLI=/path/to/effectcraft-cli ./build.sh hero          # PASS/FAIL against refs/hero-1s.png
EFFECTCRAFT_CLI=/path/to/effectcraft-cli ./build.sh hero --bless  # accept a deliberate change
```

Scripts must be run by absolute path (build.sh does this) and may only `#include` files in
their own folder, which is why scenes live at the top level.

## How JSON and JSX combine here

- **JSON** is the vocabulary: every step is an EffectCraft command with JSON params,
  `app.run("shape.newShape", {kind: "ellipse", size: [600, 600]})`.
- **JSX** is the grammar: variables, maths, loops and `if` decide *which* commands run with
  *which* numbers (sizes from the comp, layouts that switch for portrait, staggered timing).
- **style.jsx** is the taste: plain values only, the 5–15 knobs a designer would touch.

## Rules

1. New look decisions go into `style.jsx`; one-off tweaks stay in the project.
2. Sizes are fractions of the comp's shorter side (or of the shape), times are seconds.
3. Every scene has a reference render; after any change run `build.sh` and look at the result.
4. `newShape()` clears the selection first: EffectCraft's shape tool otherwise adds the new shape
   *into* the selected shape layer.
