# Verify: the check before Elias sees anything

Rule: measure, don't eyeball, then also look. Fix what the numbers show and re-check. Never
hand him an unchecked attempt.

## 0. Lint the animated range (always, first)

```text
lint_frame {comp, start: <first key>, end: <last key>}                 # whole animation
lint_frame {comp, start: <transition start>, end: <its end>, step: 0.0333}  # every frame of a transition (1/fps)
```

Required before handover: 0 errors, and every warning that stays listed in your handover, one
line each (rule · layer · why it stays); nothing left unexplained. Rules that replace looking at
renders: `cut-off` and `nested-cut-off` (layers inside precomps measured in this comp's frame,
and clipped at the precomp's edge), `text-off-centre` (text and its card/pill, measured at the
text's rest pose, not mid-pop; several texts on one card count as one block; run the problem's
`fix`, a `prop.set` of Position in the text's own units), `exposed-edge` (an empty strip at a
frame edge, or a gap between two shots in a transition), `exit-at-cut` (a full-screen cutaway,
own BG over the footage, that fades or moves out into its last frames, or is gone before the
comp ends: hold to the end and hard-cut; the notes say whether lint read the comp as
full-screen or overlay; it checks the comp's end whatever `start`/`end` you pass),
`text-overlap` (stacked words), `text-too-small`, `low-contrast`, `outside-title-safe`,
`hidden-visible`, `off-accent` (below; an error on keys you made). Each problem says which
layer, when, and how to fix it.
Re-render only to look at taste, after lint is clean.

## 1. Frames (always)

```sh
nice -n 10 $EC run out/a.ecproj comp.open '{"comp":"Main"}' render.contactSheet '{"count":12,"path":"/abs/out/contact.png"}'
nice -n 10 $EC render-frame out/a.ecproj --comp Main --time 1.2 --max-side 960 --out /abs/out/f036.png
nice -n 10 $EC render out/a.ecproj --comp Main --format h264 --resolution half --out /abs/out/a.mp4
```

Over MCP: `render_frames {count: 12}` (one labelled sheet; `overlays: ["bounds"]` tags every
layer's box), `render_preview {time, region}` for a detail at full resolution. Read the images.

**Transitions, strict (24 Oct: a stacked QUICK/FAST swap passed two reviews):** for every swap,
slide, send and pop, lint EVERY frame of it (section 0, `step` 1 frame: `text-overlap` catches
stacked words, `exposed-edge` the gaps). Render a zoomed strip (`render_frames {start, end,
region, max_side: ≥ 640}`) only for what lint can't measure (letter shapes, a level baseline)
and judge it as typography; "it moves" is not a pass. Subagents paste the lint output (and the
strip's path if they made one) in their report.

## 2. Eases are his Graphs

In the app or the MCP (required): `taste_check {comp, start, end, problems_only: true}` →
`summary.line` (✅ · 🟡 · ❌) and per move `moveType`, `verdict`, `criteria`, `message`, `fix`.
Run each `fix` (`command_run taste.apply …`) or say why not; `clean` must be true. Thresholds
(learned from his comps, 25 Oct): entrance peak ≤ 30 %, exit ≥ 75 %, on → on and scrub 30–70 %,
fade-in ≤ 50 %; fastest frame ÷ average ≤ 1.3 + 2.05 ln(frames); ≤ 18 % of the frame width per
frame (exits ≤ 22 %); an entrance/exit is read from what the layer places (a rig's children)
being off frame, a scrub is a one-axis scale from an edge anchor (progress bar, wipe);
entrances spend ≥ 30 % of their frames on the last 10 % of the travel. ❌ blocks only for move types with ≥ 2 approved
curves (`taste.profile` → `moveTypes[].blocks`). `ease_graph` draws one property.

Saved project, no app:

```sh
python3 <skill>/scripts/check_graphs.py out/a.ecproj --comp Main --md out/graphs-check.md
```

Lists every key pair that changes value and the Graph it matches (influence within 1 %,
normalised speed within 2 %), Expo In-Out included (influence from the move's duration).
Target: 0 unmatched. Anything unmatched gets a line in your notes: why, and whether Elias should
save a new graph.

## 3. Timing

- With a voice (required): the comp has its speech map (`speech.import {path}` once, from
  `speech-map`; `lint_frame` notes say "off-accent skipped" when it's missing: fix that first).
  `speech.accents {}` → every speed peak with its nearest stressed syllable and `offsetFrames`;
  `hit` = within 1 frame. `off-accent` in section 0's lint must be clean; move peaks with
  `keys.alignPeak`, never by re-rendering to watch.
- Without a voice (a reference clip): compare peak frames with the reference's motion peaks (the
  R2 scorer's `events`).

## 4. Choreography

`get_motion {}` (or `$EC exec comp.motion '{"comp":"Main"}' a.ecproj --json`): each layer's
segments and a one-line summary. Check against the brief: order, directions, holds, that
chained moves don't stop dead between them (summed speed never hits ~0 in a hand-off), that no
element exits during its own entrance, that `overlaps` are intended.

Against a brief's check table (positions, scales per frame): **read the rig's values**
(`$EC get <comp> <layer> transform/position --time S --project F`, or `prop.get {time}` in the
script) instead of detecting elements in pixels; pixel detectors latch onto the wrong row
(R2 round 1). Remember parented values are in the parent's space: add the stacked nulls up.
In a script: `app.run("prop.get", {layer: L, path: "transform/position", time: t}).value` per null;
from the shell `$EC get … --json` (it prints JSON, not a bare number). When no frame is at rest
(a zoom starts before the moves end), measure sizes and colours with the zoom keys switched off.

## 5. Design lint

Done in section 0 (the same `lint_frame` over the range). Fix every error; explain any warning
you keep.

## 6. Against a reference

- Same size, fps and length as the reference; frame 0 = the reference's first frame.
- Single frames: `render_compare {a: {path: "ref/f036.png"}, b: {comp, time}, max_side: 960}` →
  SSIM, PSNR, mean_abs, the diff heatmap and `diffBounds`. `region` to check one element.
- A whole clip: the R2 scorer, `~/Developer/lab/R2-blind-rebuild/score/score_video.py --ref
  <ref dir> --render out/a.mp4 --json out/score.json` (look SSIM, motion-energy r and lag, event
  timing, one combined score). Read the components, not just the total.
- Per element: crop reference and render to the element's box and compare zones (centre, near the
  rim, top/bottom) in mean RGB. That is how the card colours got to ~3/255 on 22 Oct.
- Stack for him: `ffmpeg -i ref.mp4 -i a.mp4 -filter_complex vstack=inputs=2 stacked.mp4`
  (same width first).

## 7. What to report

Run `handover_check {comp}` once when you're done, fix everything it lists in one pass, run it
once more, and hand over only with `ready: true`. No key changes after that (a reply's `notice`
says if you made one; then one more run). Paste its remaining warnings, one line each with why they stay.

- A stacked video or contact sheet (SendUserFile, he's often on his phone).
- One line of numbers (score, SSIM, motion r, peaks within 1 f, graphs matched x/y).
- What you're unsure of, at most one question.
