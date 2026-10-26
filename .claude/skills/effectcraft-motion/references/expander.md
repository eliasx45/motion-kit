# Expanding Elias's prompt into a builder brief

Elias writes a line ("4 glass cards slide in, one per question, then zoom out"). A builder needs
the brief format that scored at the ceiling in lab R2 (22 Oct): every number given, one null per
move, keys + Graph per move, mechanisms named. This page turns the first into the second.

R2's finding behind it: builders execute a precise brief almost exactly (three builders on one
brief land within 0.5 points of each other), so **the result is as good as the brief's numbers**.
Vague words get averaged into generic motion; numbers come back as written.

## Inputs, in order of authority

1. **His words** (what happens, in what order, anything he names).
2. **The voice** for the section: `scripts/fork/speech-map MEDIA --start S --dur S --fps F --out
   map.json` (Scribe → MFA, stressed syllables to 0.15 f). Never ask him to transcribe.
3. **A reference clip**, if he gives one: then it's a rebuild. Prefer one sighted agent that
   measures and builds; or describe it (brief-template.md, "Describing a reference").
4. **A FigCraft design**, if there is one: it owns sizes, colours, radii, shadows (figcraft.md).
5. **His taste** (taste.md) and the 8 reference comps (`motion-kit/references/`) for everything
   he didn't say. Never his old projects.

## Steps

1. **Beats from the voice.** One beat per thing he wants shown; anchor each to the word that
   carries it. A list of questions or items → one beat per item, peaking on its first stressed
   word (Moon Edits S11: the row steps peak on "WHO" / "HOW" / "HOW", 0–4 f before the vowel).
2. **Layout** from a reference comp or his design: name the comp you borrow from. Sizes in px at
   the comp size, text ≥ h/30, safe margins.
3. **Look** from taste.md: dark navy background (never purple), card bodies a 4-Color Gradient
   with dark inner shadows, 1 px hairline ~32 % white, no glow he didn't ask for, his palette for
   the project (10-10 = P01 Clock blues). Real images or `PLACEHOLDER <what>`.
4. **Moves:** one row per move: layer · property, keys (frame: value), Graph. Graph by move type
   (SKILL.md table, it wins over this line): invisible → visible Expo Out 1 (Elias) + Entrance fade, on → on Expo In-Out (sharper the longer),
   build-ups Slow launch, punches Smooth emphasis, exits Fast out + 8 f opacity fade (overlays only; full-screen cutaways hard-cut). Typical
   lengths: entrances 15–26 f, steps 35–45 f, exits 8–12 f.
5. **Timing:** `python3 scripts/peak_keys.py map.json events.json --md` puts each move's speed
   peak on its stressed syllable (vowel − 1 f) and prints the moves table. Then apply overlap: the
   next move starts at ~60 % of the previous; rows cascade 1 f.
6. **Rig:** CTRL null per scene; overlapping moves on one property → stacked nulls (the recipe in
   effectcraft-api.md); name layers like his (structure.md); a comp marker per beat with its words.
7. **Not there:** list what a builder might add (glow, bounce, shadows, drift).
8. **Check line:** the peak frames on their words, graphs 100 % (`check_graphs.py`), one or two
   positions at rest.
9. **Unsure:** at most 3 assumptions, each a one-line question for Elias, with your default.

## Output format (≤ 40 lines)

```
# <scene>: <one line>
Comp, size, fps, frames (0-based), audio (file, offset).
**Picture.** background; elements with sizes, colours, fonts (by measured width), positions at rest.
**States.** (opacity / colour, values)
**Rig.** CTRL → nulls → elements; what parents what; what zooms.
| Layer · property | Keys (frame: value) | Graph | Peak (on word) |
**Not there.** …
**Check.** …
**Unsure.** 1–3 lines.
```

Hand it to a builder with SKILL.md § Briefing a subagent. Show Elias the brief's beats and the
"Unsure" lines before building when the scene is new to him; skip that when he said "just do it".
