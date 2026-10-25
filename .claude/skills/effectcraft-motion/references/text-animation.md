# Text animation: Elias's rules (24 Oct)

Every rule is one of his corrections from the 24 Oct build. Check each transition frame by frame
([verify.md](verify.md#1-frames-always), strict transitions).

## Words appear as he says them

- Each word pops on its own spoken word (Scribe word times), never the whole line at once.
- Pop: scale 0 → 100 from the word's own centre (anchor at the word's centre), **Snap in
  (Devin)**, ~6 f; opacity 0 → 100 in 2 f.

## Word swap (substitution)

- Old and new word roll through a **clipped word window** (track matte / mask the size of one
  word) with the **same ease (Fast In)**, one line-height apart, so two words are never readable
  at once.
- Order: swap in place first; the line slide starts after the new word lands (**Expo In-Out
  (Elias)**); the next words roll in past the slide's peak.
- Check: no frame with both words legible, no half word outside the window, baseline level.

## Words that travel together (typed prompt → chat bubble)

- One layer per word, all on the same 2 keys; delay ≈ **0.35 f per word** via
  `valueAtTime(time - d)`, the far end leading. 1 f per word was "too much".
- His custom ease for that move: speed 0, out influence 25 %, in influence 65 %. Not a saved
  Graph yet: list it for him to save (`cease()` until then).

## Typing

- Source Text expression from the word times (Scribe), so words type as he says them.
- Caret solid while typing, blinking when idle.
- Caret and text parented to the input box, so they rise and fade with it.

## Cuts and imports

- Text is fully gone one frame before a cut.
- After importing a text card (Motion Library), check for stray Drop Shadow / style copies:
  they show as ghost words ([effectcraft-api.md](effectcraft-api.md#gotchas)).

- **Text inside a pill (24 Oct, 02 Years Off):** with his Slide In / Bounce In presets, put the text's In marker on the pill's pop, ~0.4 s long. `text.apply sync` on the word gave a 2 s In starting 0.3 s before the pill: "too slow and starts too early".
- **Text centred in its pill/card/tile (24 Oct, 04 Gatekeep, "fix the text centering … everywhere"):** centre the **ink** (rendered pixels), not the text box: caps sit 4–6 px low otherwise. Measure with `scripts/pill_text_centre.py groups.json out.json` (solo transparent renders, finds a rest frame, prints dx/dy), shift the text layer by it, re-measure to ≤ 0.5 px. Check every pill in the project, not just the one he points at.
- **Subtitles / captions (24 Oct, Tyson 06):** no punctuation (no commas or full stops: "remove punctuation"), SF Pro Bold ~84 px ("make the text captions bigger"), each word just appears as said, no pop (he kept that). Subtitles replace a graphic, they don't sit beside one (he had the kit card removed).
