# Handoff: the motion-kit agent

You are taking over from a cloud Claude session (21 Oct 2026) that built this kit with Elias.
Read this file, then `CLAUDE.md` (the rules), then `CATALOG.md` (what exists). Work from Elias's
Mac, which has what the cloud didn't: his Motion Library (token and cache), the footage and
library art under `/Users/elias/…`, the EffectCraft app and his fonts.

## Who you're working with
- Elias edits heavily animated YouTube/explainer videos in EffectCraft (his fork of a pure-Rust
  After Effects-like app). Goal: automate his editing with AI, by building a reusable kit one
  thing at a time.
- He's learning JSON/JSX. Teach as you go: explain in plain words what you did and why, point
  out patterns, and say when there's a higher-leverage way. Predict where he's heading and
  propose ambitious next steps, but ask before big moves.
- He often writes short or typo-heavy messages; read for intent. When he asks for a summary,
  keep it ultra concise.
- **Deadlines come first.** During an edit, use what the kit has and "inbox" new things
  (CLAUDE.md, "Using the kit in a live edit"). Never stop his edit to build kit features.
- Decisions are his: agents propose, he answers yes / no / merge in one word. Never build a
  primitive he hasn't approved.
- He likes seeing results: render and show (GIF/MP4/contact sheet) rather than describe.

## Repos and machines
- **motion-kit** (`github.com/eliasx45/motion-kit`, private, branch `main`): this repo.
- **EffectCraft fork** (`github.com/eliasx45/effectcraft`, on the Mac at
  `~/Developer/effectcraft`). Its `CLAUDE.md` and `docs/fork/agent-builds.md` have the fork's
  rules: cargo check and focused tests with `CARGO_BUILD_JOBS=4`, no `cargo xtask ci` unless he
  asks, merge (never rebase), land on `main`. **Don't queue anything for upstream** (he said no).
- `EFFECTCRAFT_CLI=$HOME/Developer/effectcraft/scripts/fork/cli.sh` is set in `~/.zshrc`. It
  rebuilds the CLI when the code changed, so it's never stale. The Dock app builds the CLI too.

## What exists (all on `main` of both repos)
EffectCraft (merged at `41985bc` and later):
- `comp.recipe` / `comp.fromRecipe`: a comp as compact JSON of only what was authored, and back.
  13 round-trip tests; rebuilds render identical.
- Fixes: `shape.fillStroke` accepts `strokeType` / `strokeBlend` / `strokeOpacity` (docs parser
  split on `/`; also fixed `view.customRgb`); script `layer.property("Position")` on a shape
  layer is the layer's Transform; script `setValue([x, y])` keeps z.
- `scripts/fork/cli.sh` and the Dock build making the CLI (see above).

motion-kit:
- `style.jsx` (the look), `lib/` primitives: `orb`, `background`, `pop`, `slideUp` (expo out,
  out influence 0 / in 100, 120 px at 1080p), `stagger` (orders, `total` + `duration` fitting),
  helpers in `lib/kit.jsx` incl. `target()` (scenes drop into the open comp at the playhead).
- Scenes `hero`, `row`, `row-slide`, `hero-vertical`; `build.sh` builds and compares against
  `refs/`. The orb/grey look was a practice style, not his video style.
- `catalog.py` → `CATALOG.md` (previews, proposals, inbox, references) + `library.json` (the kit
  as an EffectCraft folder library: `library.addFolder {path: <kit>}`). Previews are 12 fps on
  purpose (size); MP4s keep full frame rate.
- `references/`: his 8 favourite comps (DJ1 Trial Rings, DJ2 Trial Toggle, DJ3 Views Counter,
  DJ4 Tilted Stats, DJ5 Card Variants, drag-drop, ig1, YouTube Zoom Out to link) as recipes +
  GIFs, each with a `<slug>.breakdown.md` (timeline, elements, exact easing, knobs, distinctive
  parts) and `<slug>.proposals.json`: 8 **templates** (whole comp with knobs) and 64 **parts**
  (distinctive pieces, even if they appear once). He considers these comps perfect as a whole:
  take them apart, never boil them down to what they share.
- `part_preview.py`: renders one part on its own (other layers off, cropped to where it draws,
  only its moment) to `references/parts/<slug>--<partId>.gif`; each part proposal records its
  `preview` settings so it can be re-rendered.

## In flight when the cloud session ended
- Cloud agents were rendering isolated previews for all 64 parts. **`git pull` first**; if some
  parts still show their whole comp's GIF, run `part_preview.py` for them (settings pattern in
  the proposals that have a `preview` field).
- Parts whose art only exists on the Mac (cursor/eye/play/share PDFs, phone bezel PNGs,
  drag-drop's hand/icons/screenshot, YouTube avatar) rendered empty in the cloud and carry a
  `previewNote`. **Re-render those here** (the files exist on this Mac), remove the note, run
  `python3 catalog.py --no-render`, commit, push.

## Next job: decompose for real (Elias asked for this explicitly)
Breakdowns and isolated previews *describe* each part; they don't yet make it a thing you can
use on its own. For every part proposal:
1. **Extract it:** `comp.recipe {comp, layers: [<the part's layers from its "preview" field>,
   plus the parents and matte sources they need]}` → `references/parts/<slug>--<partId>.recipe.json`.
   Check `unsupported`: references to layers left out must be added back or the part is not
   self-contained.
2. **Prove it stands alone:** `comp.fromRecipe` it into an empty project, render its GIF, and
   compare with the isolated preview (`references/parts/<slug>--<partId>.gif`). Same look and
   motion = done; otherwise fix the layer set.
3. **Make it droppable:** a part recipe can then go into any comp at the playhead (a small
   `usePart(id, {at})` helper in `lib/` that builds the part's comp from its recipe and nests or
   copies its layers into the target comp; propose the helper to Elias first, it's a primitive).
4. Record `"partRecipe": "references/parts/<slug>--<partId>.recipe.json"` in the proposal and
   show it in the catalog (add a column or a link in `catalog.py`).
Templates (whole comps) are already usable as recipes; parts are what's missing.

## Open decisions (ask Elias, one word each)
1. The proposals in `CATALOG.md` (templates first: which 2–3 he'd use soonest).
   Earlier suggestions from the cloud session: `darkStage` and `accentGlow` → merge into
   `background` / `style.jsx`; `phoneMock` → stays a reference.
2. EffectCraft fixes found while converting (offer, then do on a branch and land on `main` when
   he's not mid-edit, since landing triggers a CLI rebuild):
   - Expressions can't call layers/groups like functions with match names
     (`layer("ADBE Root Vectors Group")(1)("ADBE Vectors Group")(1)("ADBE Vector Shape")` →
     "not a callable function"); `.content(1).content(1).path` works. This is why drag-drop's
     drag never plays.
   - Recipes don't carry comp markers (YouTube's `PAGE MOVE START/END` expressions) or random
     seeds (DJ3's wiggle, DJ5's Scatter noise), so those two rebuild "not exact".
   - `prop.set` with `[x, y]` on Scale stores `[x, y, 0]`.
   - A relative script path fails ("no folder to look in"); scripts must run by absolute path.
   - `comp.cropToRegionOfInterest` moves layers but not effect points like CC Light Sweep's
     `center`, so `part_preview.py`'s crop loses the sweep. Six previews (marked in their
     `previewNote`) were rendered full frame and cropped afterwards instead; re-rendering them
     with `part_preview.py` loses the sweep until this is fixed (fix in EffectCraft:
     `crates/engine/src/commands/comp_more.rs`, shift point-type effect params with the layers).
3. Building approved primitives, one at a time (CLAUDE.md, "Building an approved primitive"):
   each must rebuild the part of the original comp it came from.

## Later (parked by Elias, don't push)
- His **speech edit system** (`~/.claude/speech-edit/SYSTEM.md`, `scripts/fork/speech-map`,
  `speech.import`, `keys.alignPeak`, Devin's 5 ease graphs): the kit's timing should eventually
  take hit times from it (`stagger`/`slideUp` launching on stressed syllables).
- Learning from his corrections via recipe diffs (snapshot the agent's version and his fixed
  version, diff them, ask why only about real changes): he said not the focus now.
