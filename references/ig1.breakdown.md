# ig1 (“Pre-comp 5”) — breakdown

Source: [`ig1.recipe.json`](ig1.recipe.json) ([gif](ig1.gif)).
Proposals from this comp: [`ig1.proposals.json`](ig1.proposals.json).

## 1. What it is
An Instagram profile on a phone flies in from the right and scrolls to its reel grid, then a light
earnings card rises over it while the phone goes soft, and the card spells out
“$100–$500 just from that video”. **10.97 s comp, 1920×1080, 30 fps.** All content ends at
**8.97 s**: the last 2 s are black (no background layer; the comp is black throughout). The work
area is 0–3 s.

The comp has only two picture layers, both precomps:
- **TAPA05 - Professional dashboard** (820×300): the card.
- **TAPA05 - Editable phone assembly** (1200×1800): the phone, its screen and the scroll rig.

## 2. Timeline
| Time (s) | Beat |
|---|---|
| 0.00–0.85 | Phone flies in from the right: x 2340 → 1452 (888 px), ease 33.33 % out / 70 % in. |
| 0.00–1.17 | Inside the screen the profile scrolls up 592.5 px (Scroll slider 197.5 → 790, easy ease 33.33/33.33): the bio and highlights pass under the header, the tab bar sticks under the username at 650 px, the reel grid fills the screen. |
| 0.67–1.10 | Card rises 32 px (y 442 → 410), ease 33.33 % out / 70 % in, fading in over 0.67–0.85. |
| 0.83 (frame 25) | Green ↗ arrow pops on the card with a damped spring (65 % → 113 % → 95 % → 100 %, settled ≈ 0.6 s later). |
| 0.83–1.10 | Phone goes out of focus behind the card: Gaussian blur 0 → 6. |
| 1.00–1.55 | Phone lifts 85 px (y 846 → 761), ease 33 % out / 65 % in. |
| 2.93 | “$100” appears (hard cut, layer in-point). |
| 3.67 | “–$500” appears right after it (hard cut). |
| 4.53–5.57 | “just from that video” drops in word by word: each word falls 35 px from above and fades in, left to right, at constant speed. |
| 5.57–8.97 | Hold. |
| 8.97–10.97 | Black (every layer has ended). |

## 3. Elements

### Main comp (Pre-comp 5)
| Element | Layers | Look | Motion |
|---|---|---|---|
| **Card placement** | TAPA05 - Professional dashboard (precomp, top) | Anchor (410, 150) = card centre | `transform/position` keys 0.67 s (1420, 442) → 1.10 s (1420, 410); out: speed 0 @ 33.33 %, in: speed 0 @ 70 %. `transform/opacity` 0.67 s 0 → 0.85 s 100 (→ 2.07 s 100), easy ease 33.33 %. |
| **Phone placement** | TAPA05 - Editable phone assembly (precomp) | Anchor (600, 900), scale 94 %. Effect “Dashboard focus - Gaussian Blur” | `transform/position` 0 s (2340, 846) → 0.85 s (1452, 846) [out 33.33 %, in 70 %] → hold to 1.0 s → 1.55 s (1452, 761) [out 33 %, in 65 %]. `effects/#1/blurriness` 0.8333 s 0 → 1.1 s 6 (easy ease 33.33 %). |
| Camera | AE Default Camera | default, no effect | — |

### Card (TAPA05 - Professional dashboard, 820×300)
| Element | Layers | Look | Motion |
|---|---|---|---|
| **Card surface** | Reference dashboard surface (shape) | Rounded rect 792×124, corner ≈ 10, fill `#f6f7f9`, centred (410, 150). Drop Shadow distance 10, opacity 9.8 %, softness 24. CC Vignette amount 17, angle of view 45 (the soft grey edges). | static |
| (hidden) dark card | Dashboard surface (shape, Video off) | 796×276 r16, fill `#242830`, stroke `#404552` 1 px, Gradient Ramp `#333845` → `#21242e`, Drop Shadow 12 / 17.6 % / 30 | not rendered (an alternate dark look) |
| **Trend arrow** | Green trend arrow (shape) | ↗ drawn as one open path: shaft (49, 182) → (66, 165), head (52, 165) → (66, 165) → (66, 179); stroke `#73c98f` 2.8 px | Expressions, cue frame 25 (0.8333 s), t = time − cue, s = 35·cos(2.6·2π·t)/e^(5t): **scale** = value × (1 − s/100) (65 % at the cue, 113.4 % at +0.19 s, 94.9 % at +0.38 s, ≈ 100 % by +0.6 s); **position** = value + [58.5, 173.5]·s/100, which keeps the arrow scaling around its own centre although the layer anchor is (0, 0); **opacity** 0 before the cue, then 100. Labelled “MotionEssence ME07 curve”. |
| **Amount** | Revenue - $100 (text, in 2.9333 s), Revenue - $500 tail (text, in 3.6667 s) | Roboto Regular 26, `#5e656e`; “$100” and “–$500” | Position expressions chain them: $100 x = Views metric's right edge (`sourceRectAtTime` left + width) + 8, y 179; “–$500” x = $100's right edge + 0. They pop in by in-point, no animation. |
| **Tail words** | just from that video (text, in 4.5333 s, out 9.9 s) | Roboto Regular 26, `#5e656e`, at (415, 179) | Text animator: Position [0, −35] and Opacity 0, Range Selector based on Words, shape Ramp Up, Ease High −50, Ease Low 100; `…/rangeSelector/offset` 4.5333 s −100 → 5.5667 s 100 (speed 193.548 both sides = linear). Words fall into place from 35 px above, fading in, left to right. |
| Spacer | Views metric (text) “100,000 views ·” | Roboto Regular 26, `#5e656e`, at (80, 179) | **Never visible**: a text animator (Position via expression [0, 24], Rotation 50, Opacity 0) with an Expression Selector “ME07 Bounce Up” (per-character delay slider 1.8) stays fully applied, in the source and the rebuild alike. Its width still positions “$100”. |
| Title | Dashboard title (text) “Professional dashboard” | Roboto Regular 30, `#1a1d24`, at (44, 133) | Same invisible animator as Views metric; never shows. |
| (hidden) | Earnings context (text, Video off) | Roboto Regular 30, `#91dbad` | Source Text expression cycles “From one video” → (2.9 s) “$100–$500 from one video” → (6.1 s) “From one video” → (7.9 s) “A few thousand dollars”. Not rendered. |

### Phone (TAPA05 - Editable phone assembly, 1200×1800)
| Element | Layers | Look | Motion |
|---|---|---|---|
| **Phone frame** | Asset 5@3x 1 (PNG 1987×4096 at 39.0035 %, parent profile, alpha-matted by Asset 5@3x 1_mask 775×1597), Fixed phone camera image (same PNG, parent phone camera), phone camera (guide) + Rectangle 53 (195×56 r28 black, the camera pill) | Black bezel with a Dynamic Island, from Motion Library PNGs | static |
| **Screen** | screen-1 1 (731×1565, roundness 100, white) at (589.26, 847.3); MATTE - Figma rounded phone screen (same rect, hidden): alpha matte for the fixed UI | white rounded screen | static |
| **Fixed header** | StatusBar (hidden), _StatusBar-time precomp (“9:41”, SF Pro Regular 17, Essential Graphics), _StatusBar-battery precomp, Right Side / Left Side, icon-back 1, yournamehere (Roboto Bold 40.64, black), Star 1 (blue verified dot `#0195f7`), icon-notification, icon-more 1, Fixed username header backing (731×134 white) | Instagram top bar | static (doesn't scroll) |
| **Scrolling profile** | 70-odd layers parented to **CTRL - Reel scroll**, all alpha-matted by MATTE - Profile scrolling viewport (731×1344): Your Name Here (Roboto SemiBold 27), stats 883 posts / 14.1K folowers / 1 000 folowing (SemiBold 33.08 + Regular 25.58), Category (`#737778`), bio “The best solutions for your business”, www.yoursite.com and “Mainstreet 19, Country 2200” (`#0180f7`), @ threadshere, Folowing / Message / more-people buttons (`#f1f2f6`), 5 highlight circles (`#e3e3e3`) labelled About, Catalog, Price, Reviews, Location | Instagram profile | moves with the scroll null |
| **Reel grid** | photo-01 … (240.65×322.21 tiles `#e3e3e3`), white Rectangle 48/49/50/51 and Exclude icons (pinned / reel badges); rows 3–5 are copies named “Reel row N - …” whose position expression adds 326 / 652 / 978 px to the original | 3-column grey grid with white badges | moves with the scroll null |
| **Sticky tabs** | Children of **CTRL - Sticky tabs**: menu-gallery, the reels/tag icons (Rectangle 44 1 … 52 1), line, Sticky tabs white backing (731×81 white) | Tab bar | Sticks once scrolled 650 px |
| **Scroll rig** | CTRL - Reel scroll (null, guide), CTRL - Sticky tabs (null) | Effects “Scroll (px)” slider and “Tabs stick after (px)” = 650 | `effects/#1/slider` 0 s 197.5 → 1.1667 s 790 (easy ease 33.33 %). Reel scroll position = value − [0, Scroll]. Sticky tabs position = value − [0, min(Scroll, Tabs stick after)]: rides with the content, then stops under the header. |
| Bottom bar | phone menu | Android-style nav (Ⅲ ○ ‹) | static |
| Hidden | 22-27, icon-network, icon-charge, Vector 34, MATTE - Figma gallery viewport | — | not rendered |

## 4. Knobs (template)
| # | Knob | Layer › path | Current value |
|---|---|---|---|
| 1 | Amount low | Revenue - $100 › `text/sourceText` | “$100” |
| 2 | Amount high | Revenue - $500 tail › `text/sourceText` | “–$500” |
| 3 | Tail words | just from that video › `text/sourceText` | “just from that video” |
| 4 | Spacer text (sets where “$100” starts!) | Views metric › `text/sourceText` | “100,000 views ·” (invisible) |
| 5 | Amount reveal times | Revenue - $100 / Revenue - $500 tail › in-point | 2.9333 s / 3.6667 s |
| 6 | Word drop timing | just from that video › `text/animators/animator/selectors/rangeSelector/offset` keys | 4.5333 → 5.5667 s; layer in 4.5333 |
| 7 | Word drop height | just from that video › `text/animators/animator/properties/position` | [0, −35] |
| 8 | Arrow colour | Green trend arrow › `contents/group/contents/stroke/color` | `#73c98f` |
| 9 | Arrow cue | Green trend arrow › transform expressions `framesToTime(25)` | frame 25 (0.833 s) |
| 10 | Card colour | Reference dashboard surface › `contents/group/contents/fill/color` | `#f6f7f9` |
| 11 | Card rise / fade timing | TAPA05 - Professional dashboard › `transform/position`, `transform/opacity` | 0.67–1.10 s, 32 px; fade 0.67–0.85 s |
| 12 | Phone fly-in | TAPA05 - Editable phone assembly › `transform/position` | x 2340 → 1452 over 0–0.85 s; lift 846 → 761 over 1.0–1.55 s |
| 13 | Phone defocus | TAPA05 - Editable phone assembly › `effects/#1/blurriness` | 0 → 6 over 0.83–1.10 s |
| 14 | Scroll amount and time | CTRL - Reel scroll › `effects/#1/slider` | 197.5 → 790 over 0–1.1667 s |
| 15 | Tabs stick point | CTRL - Reel scroll › `effects/#2/slider` | 650 |
| 16 | Username | yournamehere › `text/sourceText` | “yournamehere” |
| 17 | Display name | Your Name Here › `text/sourceText` | “Your Name Here” |
| 18 | Posts / followers / following | 883, 14.1K, 1 000 › `text/sourceText` | “883”, “14.1K”, “1 000” |
| 19 | Bio lines | Category, The best solutions for your business, www.yoursite.com, Mainstreet 19, Country 2200, @ threadshere › `text/sourceText` | as named |
| 20 | Highlight labels | About, Catalog, Price, Reviews, Location › `text/sourceText` | as named |
| 21 | Status-bar time | _StatusBar-time › ✏️ Time › `text/sourceText` | “9:41” (was an Essential Graphics control) |
| 22 | Reel tile colour (or images) | photo-01 … › `contents/group/contents/fill/color` | `#e3e3e3` |

## 5. Distinctive parts
| Name | What it is | From | Call | Overlaps |
|---|---|---|---|---|
| `springPop` | Expression spring, no keyframes: scale = 1 − 35·cos(2.6·2π·t)/e^(5t) % from a cue (65 → 113 → 95 → 100 %), hard opacity cut on, position compensation so it scales around its own centre | Green trend arrow transform expressions | `springPop(layer, {at, amplitude: 35, frequency: 2.6, decay: 5, center: [58.5, 173.5]})` | `pop` (keyed 115/95 with fade); could be `pop(layer, {curve: "spring"})` |
| `wordDropIn` | Words fall 35 px from above and fade in, left to right, at constant speed (range selector by words, Ramp Up, ease high −50 / low 100, offset −100 → 100) | just from that video › Animator 1 | `wordDropIn(textLayer, {at, duration: 1.0333, height: 35})` | none (text-only entrance) |
| `trailingLabel` | Text chained to the right edge of the text before it (`sourceRectAtTime` + gap), so “$100”, “–$500” line up whatever their width | Revenue - $100 (+8), Revenue - $500 tail (+0) | `trailingLabel(label, anchorText, {gap: 8})` | same id as dj3 `trailingLabel` |
| `softRiseFade` | Small rise into place (32 px) on 33 % out / 70 % in, with a quick 0.18 s fade | Card position + opacity | `softRiseFade(layer, {at, distance: 32, duration: 0.43, fade: 0.18})` | `slideUp` (expo out 0/100, 120 px, 1 s): better as slideUp options `{distance, duration, outInfluence: 33.33, inInfluence: 70}` |
| `focusShiftToCard` | When a card lands, the layer behind it blurs 0 → 6 in 0.27 s, so the eye goes to the card | Phone precomp › Dashboard focus blur | `focusShiftToCard(backLayer, {at, amount: 6, duration: 0.27})` | `defocusIn` (dj3) is the opposite (blur → sharp on everything) |
| `scrollRig` | Null with a “Scroll (px)” slider drives a long page up inside a matte, plus a second null that follows until “stick after” px and then stays (sticky tab bar) | CTRL - Reel scroll, CTRL - Sticky tabs, MATTE - Profile scrolling viewport | `scrollRig(comp, {layers, sticky, from: 197.5, to: 790, at, duration: 1.1667, stickAfter: 650})` | none |
| `phoneFlyInScroll` | Phone enters from off-screen right (888 px, 0.85 s, 33/70) while its screen scrolls, then lifts 85 px | Phone precomp position + scroll slider | `phoneFlyInScroll(phone, {at, from: "right", distance: 888, lift: 85})` | `slideUp` (direction and easing differ) |
| `instaProfileScreen` | Editable Instagram profile screen: fixed header, profile stats, bio, buttons, highlights, sticky tabs and a reel grid built from repeatable rows (+326 px per row) | the phone assembly's screen layers | `instaProfileScreen(comp, {username, name, posts, followers, following, bio, highlights, rows})` | `phoneMock` holds it |
| `phoneMock` | Phone frame (PNG bezel + camera pill) with a rounded matte screen | Asset 5@3x 1, phone camera, screen-1 1, MATTE - Figma rounded phone screen | `phoneMock(comp, {screen, x, y, scale})` | same id as proposals.json `phoneMock` |
| `earningsCard` | Light rounded card (`#f6f7f9`, soft shadow, vignette edges) with a green ↗ and grey amount text | Professional dashboard precomp | `earningsCard(comp, {amount, tail, x, y, at})` | none (dj3 `statCard` is the dark version) |

## 6. Rebuild notes
- **Phone frame footage is missing off Elias's Mac**: `Asset 5_3x 1_24-398.png` and `…24-545.png` live in `/Users/elias/Library/Caches/EffectCraft/Motion Library/blobs/…`. In a rebuild here the bezel and Dynamic Island don't show (white rounded screen only).
- **Essential Graphics** on `_StatusBar-time` don't survive the recipe; publish the Time text again if the template should expose it.
- **Views metric and Dashboard title never render** (their animator holds Opacity 0 fully applied). They look like a planned “bounce up” intro that ended up off. Views metric still matters: its width places “$100”.
- Earnings context and the dark Dashboard surface are hidden leftovers.
- Fonts: Roboto (Regular/SemiBold/Bold) and SF Pro (status time) must be installed or text reflows; the chained amounts follow the new widths automatically.
- Shape strokes use an Offset Paths expression (`-stroke width / 2`, Figma inside-stroke import); harmless but makes the shapes slower to evaluate.
- No random seeds: the rebuild is exact (PASS, inf dB).
