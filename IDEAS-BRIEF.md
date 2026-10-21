# Brief: help Elias get AI to make motion he likes, faster

You're an ideas partner. Elias wants **concrete, ambitious ideas** for getting AI to produce
animation he likes with less back-and-forth. This brief is everything tried and decided so far
(cloud session, 21 Oct 2026). Read it, look at the linked files, then propose.

## The situation
- **Elias** edits heavily animated YouTube/explainer videos (many elements, kinetic,
  voiceover-driven, not "basic lower thirds"). Often on deadlines. He's learning JSON/JSX to
  automate his own editing. He judges by eye: he wants to *see* results, not read about them.
- **EffectCraft** (his fork, `github.com/eliasx45/effectcraft`): a pure-Rust After Effects-like
  compositor. Everything is an engine command (JSON params) usable from the CLI, the app's
  control channel, MCP, and JSX scripts (`app.run(id, params)`). Strong agent tooling already:
  `render_frames` contact sheets, `comp.motion` (plain-language motion summary), `lint_frame`
  (design lint incl. off-beat keys), `render.compare` (pixel diff), speech maps, `keys.alignPeak`.
- **Claude agents drive it**: on his Mac (Claude Code + CLI, kept current by
  `scripts/fork/cli.sh`), and in cloud sessions.

## The core problem
Opus doesn't one-shot designs/animations he likes. Taste isn't in the model; when it works in
one shot it doesn't look at what it made; and his past work wasn't readable by agents (they
screenshotted Motion Library cards and guessed).

## What we built (all in `github.com/eliasx45/motion-kit`)
1. **A kit: style + primitives + scenes.** `style.jsx` holds the look (colours, sizes as
   fractions, timing, curves); `lib/` primitives (`orb`, `background`, `pop`, `slideUp` with his
   expo-out 0/100 curve, `stagger`); scenes are ~10-line JSX built from them. Pattern taught:
   **JSON = vocabulary** (engine commands), **JSX = grammar** (loops, maths, `if`), **style file =
   taste**. Scenes drop into his open comp at the playhead (`target()`), adapt to portrait.
2. **Proof by pixels.** `build.sh` rebuilds a scene and compares to a reference render. The kit
   rebuilt our hand-made comp with 0 changed pixels; a 0.5 px drift was caught this way.
3. **Recipes (EffectCraft `comp.recipe` / `comp.fromRecipe`).** A comp as compact JSON of only
   what was authored (structure, values by path, keyframes with exact easing, effects, styles,
   expressions), and back. 43 KB project → 3 KB recipe; rebuilds render identical. This is what
   lets agents read his work instead of guessing.
4. **His 8 favourite comps converted** (`references/`): recipes + GIFs, then **taken apart**:
   per comp a breakdown (timeline, elements, exact easing, knobs, distinctive parts) and
   proposals: **8 templates** (whole comp with knobs: texts, numbers, colours, timing) and
   **64 parts** (every distinctive move/element, even if it appears once: `stampSlam`,
   `blurCut`, `rayFan`, `wordDropIn`, `scrollRig`, `zoomOutToPage`, `dashedConnector`,
   `cardGridStack`, `springPop`, …), each with an isolated preview GIF (only its layers, only its
   moment, cropped; `part_preview.py`).
5. **A visual catalog** (`CATALOG.md`, generated): primitives, scenes, proposals, inbox,
   references, with previews; the kit also appears in EffectCraft's Motion Library panel
   (`library.json`).
6. **Workflow rules for agents** (`CLAUDE.md`): kit first; looks only in `style.jsx`;
   proportional sizes; look before saying done; **agents propose, Elias decides in one word**
   (yes / no / merge); during a deadline, use the kit and "inbox this" (save a recipe + one line)
   instead of building.

## Decisions and lessons (don't re-propose the rejected ones)
- **He wants his comps kept whole AND decomposed into unique parts.** A first pass that only
  extracted what *repeats across* comps was wrong: it reduced 8 comps he considers perfect to a
  common denominator. The test is "would he reuse it on its own".
- **Part previews must show the part alone**, not the whole comp it came from.
- **Deadline first.** Never interrupt an edit to build kit features.
- **Learning *why* he corrects things** (snapshot the agent's version and his fixed version,
  diff the recipes, ask why only about real changes) is a good idea he **parked**: inferring
  reasons needs reasoning over video + transcript + past animations; "not the focus now".
- **Generic mining of his edit history** (his existing `loopd` miner) produced noise: 4,626
  candidate rules, 1 active. Rules that worked all came from chat, verified by an agent
  rebuilding the scene from the rule alone.
- Previews at 12 fps are fine (size); MP4s keep full frame rate for judging easing.
- No upstream PRs for now. Fork work lands on `main`.
- GIFs and EffectCraft fixes: background agents are welcome; he compiles/tests at night.

## His other system: speech edit (`~/.claude/speech-edit/SYSTEM.md` on his Mac)
An "apprentice editor" for talking-head videos: hear (word + stressed-syllable timing to the
frame via Scribe + MFA) → understand (emphasis ranking, barely trained) → storyboard (Devin-style
board in FigCraft) → he approves → build one scene at a time (only Devin's 8 scene types, every
move on one of Devin's 5 ease graphs, `keys.alignPeak` puts speed peaks on syllables) → lint
(off-accent, overlaps, safe areas, an "interrupt" every 10–15 s) → he reviews → learn (rules
from chat work; the "why?" strip is half-built; `loopd` is noise). Known rules include: Fast In
11.5/97.8; slide-up card row (launch on the syllable, 120 px, land at 26 f, 1 f cascade);
caption glow preset at 133 %; exits fade, never hard-cut; 2:3 post cards with a 1 px hairline.
The kit and this system are two halves: the speech system knows **when**, the kit knows **how**.

## Open threads (state as of handoff)
- Proposals await his decisions (templates first). Building approved primitives, each proven by
  rebuilding the part of the original it came from.
- "Decompose for real": each part becomes its own recipe that rebuilds alone and can be dropped
  into any comp (Mac agent, `HANDOFF.md`).
- EffectCraft gaps found: expressions can't call layers with match names (drag-drop's drag never
  plays); recipes lack comp markers and random seeds; crop moved effect points (fixed, untested).
- Some library art only exists on his Mac, so cloud renders miss it.

## What we want from you
Ideas for getting AI to create motion he likes **faster** (fewer rounds, less of his time,
higher hit rate), building on what exists rather than restarting. For each idea:
1. **What it is** in two sentences, and **what it would feel like for Elias** on a real edit.
2. **Why it would raise the hit rate or speed** (which failure it removes).
3. **What it builds on** here (kit, recipes, references, catalog, speech system, EffectCraft
   commands) and **what's missing**.
4. **Cost** (rough: hours / days / weeks of agent work) and **risk** (what could make it flop).
5. **A first experiment** small enough to try this week, with how we'd know it worked.

Rank them by leverage. Mix quick wins with a few ambitious bets. Some directions worth
considering (not limits): turning the 64 parts into a vocabulary agents compose from a script
or voiceover; taste models trained on his yes/no answers and A/B picks; generating several
variants and letting him pick fast; using his references as few-shot examples at build time;
self-critique loops with renders and lint; templates filled from data; tying the speech
system's timing to the kit's primitives; fine-tuning or hill-climbing an agent's system prompt
on his choices (see `github.com/browser-use/rl-env-use` and EffectCraft's `evals/agent/`
exam, which scores agent work with deterministic checks).

Then **ask him** which 2–3 to pursue. Keep explanations plain; he's learning.

## Where to look
- Kit: `README.md`, `CLAUDE.md`, `CATALOG.md`, `style.jsx`, `lib/`, `references/*.breakdown.md`,
  `references/*.proposals.json`, `HANDOFF.md`.
- EffectCraft: `docs/agents.md` (agent tooling, recipes, speech maps, lint, motion summary),
  `docs/libraries.md`, `evals/agent/README.md` (agent exam).
