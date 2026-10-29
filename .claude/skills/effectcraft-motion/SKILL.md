---
name: effectcraft-motion
description: Build motion graphics for Elias in EffectCraft so they look and move like his style on the first try. Holds his taste rules (his Graphs eases, Expo In-Out, overlap, exits that fade, no glow he didn't ask for, 4-colour card bodies, hairlines instead of strokes), how to write the JSX/JSON (app.run engine commands, recipes, property paths, time bases, eases), how to structure layers (scene prefix, CTRL null, beat markers) and the check that is required before showing him anything (lint over the range, speech-map accents, then render, compare with the reference). Use whenever you write or edit an EffectCraft script, recipe or command batch; build, rebuild or retime an animation, card, scene, title or motion-kit primitive for Elias; recreate a reference clip in EffectCraft; or brief a subagent that will. Use it even when he only says "animate this", "make it move", "rebuild this" or "add X to the comp", and when he asks you to read or learn from changes he made to a comp.
---

# EffectCraft motion, Elias's way

Elias edits YouTube and VSL videos in a style based on Devin Jatho's. He judges two things:
**does it move like him** (his eases, overlap, timing on the words) and **does it look like his
reference** (no AI polish on top). Every rule below is one of his corrections, dated.

This is v0 of a skill that a loop keeps tuning (lab R2: agents rebuild Moon Edits from a brief,
blind, scored against the video). When you learn something that would have saved a round, add it
here in one line with the date.

## The 6 steps

1. **Where**: your own project file, never his comps (below).
2. **Brief**: expand his line into a brief before any code, **every build, also when you build it
   yourself** ([expander.md](references/expander.md): voice → stressed syllables → keys, ≤ 40
   lines, format in [brief-template.md](references/brief-template.md)). Skip only for tweaks with
   nothing to time ("move it 10 px", "make it blue") (26 Oct, Elias: expander first, always).
   **On-screen word ↔ spoken word:** for every word that pops or shows (captions, list rows, pill
   text) write which spoken word it lands on and find its time with `speech.find` / the speech
   map. A caption word is not always its own spoken word: he often staggers caption words on
   the beat instead. When the brief doesn't say which, ask him before building (A/B 25 Oct, T3:
   both arms put each caption on its own word, he had them ±7 f off, on the beat).
3. **Look**: copy the reference, add nothing (§ Look).
4. **Move**: every key pair gets one of his Graphs (§ Motion).
5. **Build**: JSX with `app.run` engine commands (§ Writing it).
6. **Check**: render, measure, compare, fix. Only then show him (§ Check).

## Where to work

- **Default: your own `.ecproj` through the CLI.** `EC=~/Developer/effectcraft/scripts/fork/cli.sh`
  (it rebuilds itself when the code changed) or the pinned copy an experiment gives you:
  `$EC script /abs/build.jsx --save-as /abs/out/x.ecproj`.
- `nice -n 10` on every CLI call, one heavy render at a time, frames at ≤ 960 px: Elias edits on
  this Mac. Full-resolution or long renders go to his PC (`pc-predator`) when a tool for it exists.
- **His live app** (control port 9877, `effectcraft-app` MCP) only when the task is his edit or
  he says so. Then work as the agent client (never `"client": ""`), in comps you made unless he
  names one of his, and never save his project. If a tool acts on his selection, read it first
  and restore it after.
- **Check which project is open (`get_state`) right before creating a comp** in his live app, and
  again if a turn runs for minutes: he switches projects while you work. Build in the open one
  unless he named another. ✅ (24 Oct: the first Graphs Lab landed in 10-10 after he'd switched to
  20-08; retro case build-in-open-project)
- Tests and experiments never talk to 9877. Use a sandbox app on another port if you need a UI.

**Rebuilding a reference? The reference wins** over every rule below: copy its halo if it has
one, and fit each measured move to the nearest Graph (`scripts/fit_graph.py`) even when the table
below would pick another. The rules are for his own new builds (R2 round 1, 22 Oct: both
conflicts cost builders time).

## Look

- **Real posts, reels, profiles, stories on screen:** follow `~/.agents/skills/video-editing/rules/real-social.md` (nothing of ours on them, real IG phone layout, Deep Glow word highlights).
- **10-10 house style (22 Oct retro, full list in `~/.hermes/profiles/editing-lead/workspace/ec/10-10 design rules.md`):**
  cards = the S3 03 Bio card (top→bottom gradient #236197→#123266→#0c1423→#04070e, gradient ABOVE the solid fill, 1 px white 32 %,
  SF Pro Display Medium 40, sentence case), ~54 px text on screen, glossy pale-blue Codex icons (no square badges),
  presenter at 104 % centred (no 125 % punch-ins under graphics, don't slide him aside unasked), no BG dim/blur without a card,
  entrances = 100 px slide, Expo Out 1 (0.1/100) + Entrance fade on opacity, 1 s. Cuts go into the part comp AND 10-10 MAIN.
- **Copy only what the reference or his design shows.** No glow, flash, drop shadow, gradient
  sheen or "polish" he didn't ask for (22 Oct: "trying to make good design makes it bad design").
  His own pill finish is the one stack he chose himself ([taste.md](references/taste.md#pills-and-tags)).
- **Card and tile bodies:** a 4-Color Gradient (a near-black point in one corner, blues elsewhere,
  placed diagonally), dark inner shadows measured against the reference, a 1 px hairline (white
  ~32 %) at most. Never a thick white outline (19 Oct: "very, very low quality").
- **Colour:** the project's palette (10-10 = the P01 Clock blues). Scene backgrounds: the mock's or his BG precomp; dark navy only in 10-10 (24 Oct Tyson: "who told u to use blue bg?"),
  **never purple**.
- **Images:** real screenshots or photos. Missing ones become a flat grey box named
  `PLACEHOLDER <what>`, never code-drawn fake art.
- **Text:** at least comp height / 30, contrast ≥ 3 : 1 over what's under it; captions bigger
  than feels right. White text on a light gradient centre fails: darken the centre or the text.
- **When a FigCraft design exists, it owns the look**: sizes, colours, radii and shadows come
  from it, not from you ([figcraft.md](references/figcraft.md)).
- **UI recreations** (app screens: Claude, ChatGPT…): rebuild as real layers: live text in the
  app's font, shape boxes, Motion Library icons (Devin Jatho/Icons), vector shapes for missing
  icons. Never keyed / cut-out screenshots (24 Oct: cut-outs gave noise and a ghost line; he
  asked for real layers).

## Motion

His 5 Graphs (Motion Library → Devin Jatho → Graphs), Expo In-Out and his 6 saved Motion Library
curves are the **only** eases (12, all in [graphs.jsx](assets/graphs.jsx)). Pick by where the speed
peak must fall; exact values in [taste.md](references/taste.md#graphs).

| Move | Graph | Peak |
|---|---|---|
| off → on, snap in on the word | Fast In | at the start |
| off → on, arrives then settles | Quick launch · soft landing | early (26 %) |
| a build-up that lands on the word | Slow launch · quick finish | late (60 %) |
| push-in / punch centred on the word | Smooth emphasis | middle |
| on → off | Fast out | at the end |
| **on → on** (moves to another visible spot) | **Expo In-Out (Elias)**, sharper the longer | middle |
| **off / invisible → visible, ANY direction** (slide up/down/left/right; always, ✅ Elias 25 Oct) | **Expo Out 1 (Elias)** on position + **Entrance fade (Elias)** on opacity (~8 f) | frame 1, long settle |
| **scale pop from 0** (cards, icons) ✅ 25 Oct | 2 f kick (out 0.1 %) + Motion Library Bounce: icon 20/3/5, card 12/3/6 ([taste.md](references/taste.md)) | the spring is the motion |
| **row of cards / thumbnails slides up** from off-screen | his card-row ease: out ~1–11 / in ~100, 25 f, 1 f cascade ([taste.md](references/taste.md#graphs)) | at the start |
| ~~soft entrance, text reveal~~ → now Expo Out 1 when it comes from invisible; Quick out, gentle land (Devin) only for a soft move that is already visible | Quick out, gentle land (Devin) | early |
| on → off, leaves at full speed (match cuts) | Launch out (Devin) | at the end |
| whip / slide transition | Whip (Devin) | middle |
| reel/card pops out of a phone (scale + position) | Reel Pop-In (Elias) *(not approved)* | at the start |

🎞️ Approved moves, 12 fps: [entrance](assets/gifs/entrance-expo-out-1.gif) · [icon pop](assets/gifs/pop-icon.gif) · [card pop](assets/gifs/pop-card.gif). Every move Elias approves gets a 12 fps GIF in `assets/gifs/` (render_frames sheet → crop → ffmpeg 12 fps, 640 px), linked next to its rule.

**⏳ Waiting for Elias (24 Oct):** the 6 saved-curve rows above are NOT approved by him yet
(`elias_ok: false` in graphs.json). Don't use them in builds until he approves them in the Graphs Lab
comp; until then the 5 Graphs + Expo In-Out are the only eases.

**See and tune them:** `scripts/graphs-lab.jsx` builds comp "Graphs Lab (Claude)", one pill per ease on
the same 1 s move. After Elias edits a pill's keys, `scripts/graphs-lab-read.jsx` returns each ease in
GRAPHS format: copy the changed ones into graphs.jsx **and** graphs.json.
**Approvals use real elements, tuning uses pills.** Whenever you ask him to approve a move or ease,
show it on real Motion Library elements at real duration and distance (~0.4–0.8 s, ~100 px); the
same abstract pill move is only for tuning or comparing eases side by side. ✅ (24 Oct, retro case
approve-on-real-elements: "a real pop-in… a reel frame from Motion Library")
To **approve** a curve, look at it on its real job: `scripts/graphs-lab-in-use.jsx` builds "Graphs Lab – in use
(Claude)", 7 × 3 s sections, each new ease on real Motion Library elements (Devin Jatho/Elements) at real
durations (notification entrance, icon pop, reel out of a phone, text reveal, card exit, whip, browser
on → on). Neither is synced with
Motion Library, and the engine's `keys.alignPeak` / `keys.peakGraphs` (peak.rs) only know the 5 Graphs
(pass the others as custom `{out, in}`).

- **Peaks land on the stressed syllable**: about 2 frames after the consonant burst, i.e. the
  vowel − 1 frame ("CON-tent" = f1281). `keys.alignPeak` puts a move's peak on a word for you.
- **Overlap:** chained moves never stop between them. The next starts at ~60 % of the previous,
  past its peak. Keep the key that's locked to a word on its word; shift the other end. Moves
  that overlap on one property go on **stacked nulls**, one move each ([effectcraft-api.md](references/effectcraft-api.md#overlapping-moves-r2-round-1-22-oct-every-builder-hit-this)).
- **Exits fade** (opacity over ~8 f), never a hard cut, unless the cut also jumps to a clearly
  different shot. **Full-screen cutaways (own BG over the footage) never fade out**: they hard-cut back to the footage or into the next comp (24–25 Oct, Tyson 05, 07, 09, 10: "don't fade out, just let it cut"). Fades are for overlays on top of visible footage. They also hold **to the comp's last frame**: "back to the footage" means the comp's end, not earlier (A/B 25 Oct: every run faded where he cuts, or left 36 f early). `lint_frame` rule `exit-at-cut` checks both.
- **Hold after landing.** No drift key after a move (it overshoots on the motion path).
- Rows of cards cascade by **1 frame**, left → right.
- **2–4 bezier keys per move**, eased with a Graph. Never one key per frame.
- Pops and springs: "add bounce" = the Motion Library Bounce tool (`toolkit_bounce`), never
  hand-made spring keys or expressions.
- **Text** (word pops, word swaps, words travelling together, typing):
  [text-animation.md](references/text-animation.md) (24 Oct).
- A move no Graph fits: build the nearest one and **list it for Elias** to save a new graph
  (`taste.propose {name, layer, path, key}` files it as ⏳; only he approves, never call
  `taste.approve` yourself). Don't invent curves, Easy Ease or the kit's generic expo. Exception: a **reference rebuild**
  whose measured moves no Graph fits takes the brief's custom eases, `cease()` in graphs.jsx
  (speed 0, given influences); check with `check_graphs.py --reference`.

## Writing it

Ranked routes (v0, the R2 loop tests this ranking):

1. **JSX + `app.run("command.id", {…})`** with the kit helpers (`motion-kit/lib/kit.jsx`) and
   [graphs.jsx](assets/graphs.jsx). Best for anything new: maths, loops and layout in JS,
   every step a validated engine command that fails loudly.
2. **Recipe JSON** (`comp.recipe` / `comp.fromRecipe`). Best for copying or adapting an existing
   comp exactly, and for hand-writing a static layout in one undo step.
3. **After Effects object model** (`layer.property("Position").setValueAtTime`). Only for what no
   command covers: it can fail silently.

The facts that cost rounds when missed (all of them in [effectcraft-api.md](references/effectcraft-api.md)):

- Keyframe times are **layer time**; pass `timeBase: "comp"` or keep layers starting at 0.
  `run_script` `setValueAtTime` is comp time. Writes snap to frames.
- `prop.set` with a time does **not** key an unkeyed property (it sets the value). Use
  `prop.addKey` (`key()` in kit.jsx).
- Point text is horizontally centred on its position: `justify: "left"` for left-aligned rows.
- Zooms: parent an oversized background to the zoom null too.
- `shape.newShape` makes a new shape layer (since `ee6e05a7`, 24 Oct); `into: <layer>` or
  `addToSelected: true` draws into an existing one. Builds before that merged into the selected
  shape layer: deselect first (`newShape()` does). New layers go on top: reorder.
  Its stroke width defaults to the Tools bar's: pass `strokeWidth` (0 for none).
- Scripts run by **absolute path** and `#include` only files in their own folder or below: keep
  every script, probes and calibration scripts too, in one folder with `kit.jsx` and `graphs.jsx`.
- Eases: `keys.velocity` takes speed in value units per second. A Graph card's speed is
  normalised; `graph()` in graphs.jsx converts it. Call `graphsFinish()` once at the end.
- **Parent last**, at a frame where the parents are at rest (`time.set`), after keying in comp
  space. Keys added after parenting are in the parent's space (a card under a CTRL null jumps
  bottom-right). Opacity isn't inherited: fade children too.
  Exception: a rig of stacked offset nulls (overlapping moves, zooms): make the nulls neutral,
  parent everything **before** any key, then key the offsets ([recipe](references/effectcraft-api.md#overlapping-moves-r2-round-1-22-oct-every-builder-hit-this)).
- Name every layer when you create it (`name`), so later steps address it by name.

The three routes render pixel-identical when done right (tested 22 Oct); the ranking is about
how often each goes wrong, not what it can do.

## Structure

Built so Elias can keep editing it by hand ([structure.md](references/structure.md)):

- Names: `<scene> <element> <n>` like his `S2 W Tag 0`, text layers end in ` T`, one
  `<scene> CTRL` null (hidden) that parents the scene's moving elements.
- A comp marker per beat with the words: `B1 · "what these pages have in common"`.
- Precomp what repeats (a card, a row item); keep one master and duplicate it.
- Sliders on the CTRL null for the knobs he'll touch (travel, delay, colour).

## Check (required before showing him)

Do all of it; [verify.md](references/verify.md) has the commands. Measure first, look second:
lint answers "is it cut off / centred / covered / on the word" without a render (25 Oct: last
week 390 `render_frames` calls and 0 `lint_frame`; Elias still caught the gaps, the off-centre
text and the precomp cut-offs).

1. **Lint over the animated range** (required): `lint_frame {start, end}` from the first key to
   the last, `step` = 1 frame across every transition. Handover needs 0 errors, and **every
   warning still there is listed in your handover with its reason** (one line each: rule, layer,
   why it stays); none left unexplained (A/B 25 Oct: runs handed over with 3 off-accent, a
   low-contrast and a title-safe warning unmentioned). It covers cut-off (inside precomps too,
   in this comp's frame: `nested-cut-off`), text off its card's centre (`text-off-centre`,
   measured at the text's rest pose; run its `fix`, the `prop.set` in the text's own Position
   units, instead of nudging by eye), empty edges and transition gaps (`exposed-edge`), exits
   into the cut or before the comp's end in a full-screen cutaway (`exit-at-cut`: hold to the
   end and hard-cut), small text, contrast, overlapping text, hidden layers.
2. **Timing** (required with a voice): the comp's speech map is loaded (`speech.import` once;
   `speech.accents` lists every peak with its stressed syllable) and `off-accent` is clean in
   that same lint: every peak within 1 frame, moved with `keys.alignPeak`. An `off-accent` on keys
   you made is an **error** (it blocks the handover); one on his keys stays a warning.
   **First frames:** keep his timing; don't move entrances onto words on your own. `appear_plan
   {comp}` (engine `speech.appearPlan`) is there when he asks for a pop on a word ("pop on
   *money*"); it isn't a default step (A/B 26 Oct: as a step it moved captions he staggers on the
   beat and started pops before the layer's in-point; timing fixes rose 10 → 15). Check `speech.get` first; no map: make one
   (`speech-map`, cached, so it never re-buys audio), never time by ear or by re-rendering.
3. **Frames, to look** (after lint is clean): one contact sheet of the whole move and one frame
   per beat. **Every transition** (swap, slide, send, pop) is linted on every frame (step 1);
   a zoomed strip (`render_frames` with `region`, ≥ 640 px) only for what lint can't measure
   (letter shapes, a level baseline), judged as typography, not "does it move" (24 Oct: a
   stacked QUICK/FAST swap passed two reviews; `text-overlap` per frame now catches it).
4. **Eases (taste check, required):** `taste_check {comp, start, end}` (MCP; engine
   `taste.check`, also lint rule `off-taste`) judges every move against his profile: ✅ his
   approved curve for that move type · 🟡 in his range but not approved (says how it differs) ·
   ❌ linear, Easy Ease, speed jump, baked keys, or outside his ranges (peak position, sharpness
   for the length, speed in % of the frame, entrance landing). Handover needs `clean: true` (no blocking ❌)
   and every other ❌ / 🟡 fixed with its `fix` call (`taste.apply`) or named with why.
   `ease_graph {layer, property}` shows the value + speed graph (send it to Elias when you ask
   about a move). Saved files without the app: `scripts/check_graphs.py` (stricter, 1:1 match).
   ✅ (25 Oct: eases were last week's #1 cost, ~200 min of his fixes)
5. **Choreography:** `get_motion` summary reads like the brief; no dead stops between chained
   moves, nothing exits during its own entrance.
6. **Against the reference** (when there is one): render at the same size and fps, stack them,
   score (`render_compare` per beat frame; the R2 scorer for a whole clip). Fix what the numbers
   show, then look again.

7. **Handover check (last, required):** `handover_check {comp}` (engine `handover.check`) runs
   the taste check and lint over the comp's animated range in one call. Run it **once, when you're
   done**; fix everything it lists in one pass, then run it a second and last time. Hand over
   only when it says `ready: true`, and list every warning it still returns with its reason.
   Change no keys after that last run (a reply's `notice` tells you if you did; then run it once
   more). Not after each fix: 4–7 runs per task cost +35 % tokens in the A/B (26 Oct); changing
   keys after a clean check is what let ❌ through (T5, T8).

**Use what exists before keying by hand:** text entrances = `text.apply {preset: "Slide In",
layers | words, sync}` (his Motion Library text presets); a Devin scene =
`library.scene {scene: "YT Zoom Out", word, swap: {"Title": "4.2M views", "thumb.png": "/path"}}`
(no `scene` lists them); bounce = `text.unitBounce` / `toolkit_bounce`. Hand keys only when no
preset or scene fits, and say so (25 Oct: ~110 min of his time last week redoing hand-built
ones with the presets).

## Learning from his hand edits

**Every time you hand a comp over in his live app**, right after the check, snapshot it:
`ec-comp-diff snap <comp id>` (dump + project path in `~/.cache/ec-comp-snapshots/`). The
`editing-retro` skill diffs these against what he finished to learn his silent fixes. When he says "read my changes" / "learn from what I did":
`ec-comp-diff diff <comp id>` prints exactly what he changed (keys, eases, masks, new layers).
Built from a saved `.ecproj` instead: `ec-comp-diff dump NAME --project X.ecproj > old.txt`, then
`ec-comp-diff diff <id> old.txt`. Write each change into taste.md as a rule (24 Oct: without a
snapshot I nearly couldn't tell what he'd fixed on the YouTube cards).

## When you correct your own tool: fix the source

Moved keys after a preset, recipe, engine command, script or skill rule gave the wrong result? That's
the recipe, not the plate (29 Oct: the lead moved Slide In 9 f earlier on "economics" and nothing
learnt). Name the real source with proof (frames, values); a late preset is often its placement (In
marker on the word start, not peak = stressed vowel − 1 f). Then
`source-fix note --source … --what … --proof …` (`--unclear` when unsure): it files one inbox card per
source and, in a Ghostex Editing chat, prints the extra **🔧 Fix the source** button for wrap_up
(never first). The fix runs in a separate chat (`source-fix start <id>`), never in the edit.

## Showing Elias

- Send the result where he is (often his phone): a stacked video (reference on top, yours below)
  or the contact sheet, with `SendUserFile`.
- Numbers in one line, what's uncertain in one line, at most one question.
- 2+ questions (whys, sister cases, which variant, where to save) → one ```questions form with one
  line of text above, never prose; never guessed reasons as choices. One question → the end-of-turn
  buttons. Format + example: editing-retro § Asking.
- Never say done before you've looked at the frames yourself.

## Briefing a subagent

**Expanding his short prompt into a brief:** [expander.md](references/expander.md) (voice →
stressed syllables → `scripts/peak_keys.py` → moves table in the ≤ 40-line format). Builders
reproduce a precise brief almost exactly (lab R2: three builders on one brief within 0.5 points),
so the brief's numbers decide the result.

Give it this skill's path, the brief ([brief-template.md](references/brief-template.md)), its own
work folder and project file, the CLI to use, and the rules: no live app, no Elias comps,
`nice -n 10`, deliver `out/*.ecproj` + render + `NOTES.md`. NOTES.md must paste the `lint_frame`
output over the animated range (step 1 frame across each transition, `off-accent` included when
there's a voice); a report without it is not done (24 Oct: a stacked QUICK/FAST swap reached
Elias). Subagents run on Opus 5.5 at medium
effort unless Elias says otherwise (22 Oct).
