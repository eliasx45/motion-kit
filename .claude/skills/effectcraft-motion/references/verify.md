# Verify: the check before Elias sees anything

Rule: measure, don't eyeball, then also look. Fix what the numbers show and re-check. Never
hand him an unchecked attempt.

## 1. Frames (always)

```sh
nice -n 10 $EC run out/a.ecproj comp.open '{"comp":"Main"}' render.contactSheet '{"count":12,"path":"/abs/out/contact.png"}'
nice -n 10 $EC render-frame out/a.ecproj --comp Main --time 1.2 --max-side 960 --out /abs/out/f036.png
nice -n 10 $EC render out/a.ecproj --comp Main --format h264 --resolution half --out /abs/out/a.mp4
```

Over MCP: `render_frames {count: 12}` (one labelled sheet; `overlays: ["bounds"]` tags every
layer's box), `render_preview {time, region}` for a detail at full resolution. Read the images.

## 2. Eases are his Graphs

```sh
python3 <skill>/scripts/check_graphs.py out/a.ecproj --comp Main
```

Lists every key pair that changes value and the Graph it matches (influence within 1 %,
normalised speed within 2 %), Expo In-Out included (influence from the move's duration).
Target: 0 unmatched. Anything unmatched gets a line in your notes: why, and whether Elias should
save a new graph.

## 3. Timing

- With a voice: `speech.accents {}` → every speed peak with its nearest stressed syllable and
  `offsetFrames`; `hit` = within 1 frame. Or `lint_frame {rules: ["off-accent"], start, end}`.
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

## 5. Design lint

`lint_frame {start: 0, end: D}` → text too small, low contrast (< 3 : 1), outside title safe,
cut off, overlapping text, hidden but on. Fix every error; explain any warning you keep.

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

- A stacked video or contact sheet (SendUserFile, he's often on his phone).
- One line of numbers (score, SSIM, motion r, peaks within 1 f, graphs matched x/y).
- What you're unsure of, at most one question.
