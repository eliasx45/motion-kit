---
name: effectcraft-motion
description: Build motion graphics for Elias in EffectCraft so they look and move like his style on the first try. Holds his taste rules (his Graphs eases, Expo In-Out, overlap, exits that fade, no glow he didn't ask for, 4-colour card bodies, hairlines instead of strokes), how to write the JSX/JSON (app.run engine commands, recipes, property paths, time bases, eases), how to structure layers (scene prefix, CTRL null, beat markers) and the check that is required before showing him anything (render, measure, compare with the reference). Use whenever you write or edit an EffectCraft script, recipe or command batch; build, rebuild or retime an animation, card, scene, title or motion-kit primitive for Elias; recreate a reference clip in EffectCraft; or brief a subagent that will. Use it even when he only says "animate this", "make it move", "rebuild this" or "add X to the comp".
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
2. **Brief**: write the beat table before any code ([brief-template.md](references/brief-template.md)).
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
- Tests and experiments never talk to 9877. Use a sandbox app on another port if you need a UI.

## Look

- **Copy only what the reference or his design shows.** No glow, flash, drop shadow, gradient
  sheen or "polish" he didn't ask for (22 Oct: "trying to make good design makes it bad design").
  His own pill finish is the one stack he chose himself ([taste.md](references/taste.md#pills-and-tags)).
- **Card and tile bodies:** a 4-Color Gradient (a near-black point in one corner, blues elsewhere,
  placed diagonally), dark inner shadows measured against the reference, a 1 px hairline (white
  ~32 %) at most. Never a thick white outline (19 Oct: "very, very low quality").
- **Colour:** the project's palette (10-10 = the P01 Clock blues). Scene backgrounds dark navy,
  **never purple**.
- **Images:** real screenshots or photos. Missing ones become a flat grey box named
  `PLACEHOLDER <what>`, never code-drawn fake art.
- **Text:** at least comp height / 30, contrast ≥ 3 : 1 over what's under it; captions bigger
  than feels right. White text on a light gradient centre fails: darken the centre or the text.
- **When a FigCraft design exists, it owns the look**: sizes, colours, radii and shadows come
  from it, not from you ([figcraft.md](references/figcraft.md)).

## Motion

His 5 Graphs (Motion Library → Devin Jatho → Graphs) plus one saved curve are the **only** eases.
Pick by where the speed peak must fall; exact values in [taste.md](references/taste.md#graphs).

| Move | Graph | Peak |
|---|---|---|
| off → on, snap in on the word | Fast In | at the start |
| off → on, arrives then settles | Quick launch · soft landing | early (26 %) |
| a build-up that lands on the word | Slow launch · quick finish | late (60 %) |
| push-in / punch centred on the word | Smooth emphasis | middle |
| on → off | Fast out | at the end |
| **on → on** (moves to another visible spot) | **Expo In-Out (Elias)**, sharper the longer | middle |

- **Peaks land on the stressed syllable**: about 2 frames after the consonant burst, i.e. the
  vowel − 1 frame ("CON-tent" = f1281). `keys.alignPeak` puts a move's peak on a word for you.
- **Overlap:** chained moves never stop between them. The next starts at ~60 % of the previous,
  past its peak. Keep the key that's locked to a word on its word; shift the other end.
- **Exits fade** (opacity over ~8 f), never a hard cut, unless the cut also jumps to a clearly
  different shot.
- **Hold after landing.** No drift key after a move (it overshoots on the motion path).
- Rows of cards cascade by **1 frame**, left → right.
- **2–4 bezier keys per move**, eased with a Graph. Never one key per frame.
- Pops and springs: "add bounce" = the Motion Library Bounce tool (`toolkit_bounce`), never
  hand-made spring keys or expressions.
- A move no Graph fits: build the nearest one and **list it for Elias** to save a new graph.
  Don't invent curves, Easy Ease or the kit's generic expo.

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
- `prop.set` with a time does **not** key. Use `prop.addKey` (`key()` in kit.jsx).
- `shape.newShape` adds into the selected shape layer: deselect first (`newShape()` does).
  Its stroke width defaults to the Tools bar's: pass `strokeWidth` (0 for none).
- Scripts run by **absolute path** and `#include` only files in their own folder or below.
- Eases: `keys.velocity` takes speed in value units per second. A Graph card's speed is
  normalised; `graph()` in graphs.jsx converts it. Call `graphsFinish()` once at the end.
- **Parent last**, at a frame where the parents are at rest (`time.set`), after keying in comp
  space. Keys added after parenting are in the parent's space (a card under a CTRL null jumps
  bottom-right). Opacity isn't inherited: fade children too.
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

Do all of it; [verify.md](references/verify.md) has the commands.

1. **Frames:** a contact sheet of the whole move, plus single frames at every beat. Look at them.
2. **Eases:** `scripts/check_graphs.py out.ecproj --comp NAME` → every moving key pair matches a
   Graph (0 unmatched, or each one listed with why).
3. **Timing:** `speech.accents` / `lint off-accent` when there's a voice; peaks within 1 frame.
4. **Choreography:** `get_motion` summary reads like the brief; no dead stops between chained
   moves, nothing exits during its own entrance.
5. **Design lint:** `lint_frame` over the range: no small text, low contrast, cut-off or overlaps.
6. **Against the reference** (when there is one): render at the same size and fps, stack them,
   score (`render_compare` per beat frame; the R2 scorer for a whole clip). Fix what the numbers
   show, then look again.

## Showing Elias

- Send the result where he is (often his phone): a stacked video (reference on top, yours below)
  or the contact sheet, with `SendUserFile`.
- Numbers in one line, what's uncertain in one line, at most one question.
- Never say done before you've looked at the frames yourself.

## Briefing a subagent

Give it this skill's path, the brief ([brief-template.md](references/brief-template.md)), its own
work folder and project file, the CLI to use, and the rules: no live app, no Elias comps,
`nice -n 10`, deliver `out/*.ecproj` + render + `NOTES.md`. Subagents run on Opus 5.5 at medium
effort unless Elias says otherwise (22 Oct).
