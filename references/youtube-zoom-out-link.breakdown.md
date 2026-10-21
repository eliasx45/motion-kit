# YouTube Zoom Out to link in description (“YouTube Card”) — breakdown

Source: [`youtube-zoom-out-link.recipe.json`](youtube-zoom-out-link.recipe.json) ([gif](youtube-zoom-out-link.gif)).
Proposals from this comp: [`youtube-zoom-out-link.proposals.json`](youtube-zoom-out-link.proposals.json).

## 1. What it is
Your full-frame 16:9 video slides up and away as the YouTube watch page rises from below and
zooms out to 100 %; a cursor glides up onto the link in the description, then the edit cuts back
to the video with a quick blur-to-sharp. **3.17 s, 2624×1430, 60 fps**, comp background black
(`Background` shape, `#000000`).

Structure (3 precomps, all editable):
- **YouTube Video** (2624×1476): the replaceable video. Today a placeholder: `#171717` plate,
  a white Play PDF icon (scaled 833.33 %) and “YOUR VIDEO · 16:9” (Roboto Regular 42, `#8c8c8c`).
  It is used twice: as the video that leaves and as the video that returns.
- **YouTube Page** (3200×2691): the watch-page details, the cursor, the avatar.
- **YouTube Avatar** (160×160): the channel photo (Tapa.jpg at 181.82 %), cropped round by a mask
  on its layer in the page.

## 2. Timeline
| Time (s) | Beat |
|---|---|
| 0.00–0.07 | Video holds full frame. |
| 0.07–2.24 | **Page move**: MOVE - YouTube page y 1827.07 → 760 and MOVE - Page scale 86.11 % → 100 %, both out 17.76 % / in 98.94 % (starts gently, then a very long glide in). The page rises from below the frame and grows. |
| 0.07–≈0.6 | The video rides up with the page and leaves through the top; between 0.18 and 0.40 it also grows (116.13 → 140 % in page space, easy ease 33.33 %) and slides to its end spot (1312, −1419.2) above the page. |
| 0.27–2.33 | Cursor glides from below the page (1170, 3112.5) to the first description link (534, 2108), out 20 % / in 88.08 % (long settle onto the link). Rides along with the page move. |
| 2.24–2.60 | Hold on the page with the cursor on the link. |
| 2.60 | Hard cut: page and video layers end; RETURN VIDEO starts, full frame. |
| 2.60–2.80 | Return video racks into focus: Gaussian blur 28 → 0 (out 20 %, in 70 %), Repeat Edge Pixels on. |
| 2.80–3.17 | Hold on the video. |

## 3. Elements
### Main comp (YouTube Card)
| Element | Layers | Look | Motion |
|---|---|---|---|
| **Colour controls** | CTRL - Global (null, guide) | Color controls: Description `#373737`, Text `#f2f2f2`, Link `#3dadd1` | Read by expressions inside YouTube Page (`comp('YouTube Card').layer('CTRL - Global').effect(…)('Color')`). |
| **Page move rig** | MOVE - YouTube page (null) → MOVE - Page scale (null, child) | — | Position 0.0667 s [0, 1827.0714] → 2.2373 s [0, 760]; Scale 86.1068 % → 100 %; both out speed 0 @ 17.76 %, in speed 0 @ 98.94 %. Expression on both: *find comp markers “PAGE MOVE START” and “PAGE MOVE END”, and play the two keys between them* (so moving the markers retimes the move without touching keys). |
| **Page** | YOUTUBE UI - editable inside (precomp YouTube Page, parent MOVE - Page scale, out 2.6 s) | anchor (0, 1989): the page's left edge at comp x 0, page y 1989 on the null | rides the rig |
| **Leaving video** | VIDEO - replace in source comp (precomp YouTube Video, parent MOVE - Page scale, out 2.6 s) | anchor (1312, 738) | Keys (page space): 0.182 s (1523.69, −1291.50) @ 116.13 % → 0.40 s (1312, −1419.2) @ 140 %, easy ease 33.33 %. At the start of the page move those values put it exactly full-frame (comp (1312, 715) at 100 %). Expression (position + scale): *follow the page move's own eased progress and travel on one straight line in comp space from the start spot to the end spot, keeping its on-screen size consistent* — see Rebuild notes: it currently errors, so the keys drive it. |
| **Return video** | RETURN VIDEO - same replaceable source (precomp YouTube Video, in 2.6 s) | anchor (1312, 738) at (1312, 715): full frame. Gaussian Blur, Repeat Edge Pixels | `effects/#1/blurriness` 2.6 s 28 → 2.8 s 0, out speed 0 @ 20 %, in speed 0 @ 70 %. |
| Background | Background (shape) | 2624×1430 `#000000` | — |

### Page (YouTube Page, 3200×2691); positions are page pixels
| Element | Layers | Look | Motion |
|---|---|---|---|
| **Page backing** | Dark Gray Solid 8 (solid 3200×2300 `#111111`, scale 100/128 %) | Mask “Page details only” keeps y ≥ 1314 of the solid (the area under the video) | static |
| **Title** | EDIT - Video title | “Claude + Instagram = $32,561”, Roboto SemiBold 54, colour from CTRL Text (`#f2f2f2`). Drop Shadow distance 2, opacity 23.5 %, softness 18; Deep Glow radius 42, exposure 0.006 | static at (520.44, 1672.39) |
| **Channel row** | AVATAR - replace inside (precomp, circular mask Ø160, scale 81.25 % at (213, 1788.5)), EDIT - Channel “Tapa” (Roboto 46, same shadow + Deep Glow), EDIT - Subscribers “17.7K subscribers” (Roboto 35) | `#f2f2f2` text | static |
| **Like / dislike capsule** | Like dislike capsule (415×108, r54, `#212121`), Like/Dislike - native outline + cuff (thumb paths, stroke `#d9d9d9` 3 px; dislike rotated 180°), Action divider (2×68 `#333333`), EDIT - Likes “39” (Roboto SemiBold 41, `#e8e8e8`) | YouTube pill | static |
| **Share capsule** | Share capsule (275×108, r54, `#2e2e2e`), Share - PDF (icon at 316.67 %), Share label (Roboto 41, `#e8e8e8`) | YouTube pill | static |
| **Description box** | Description - editable size and corners (3000×649, roundness 34, anchor at top edge (0, −154); fill from CTRL Description `#373737`) | grey rounded box | static |
| **Description text** | EDIT - Views “4,334 views  Sep 28, 2026” (Roboto 38), EDIT - CTA “Join my Live Free training on how build a Faceless Instagram Page:”, EDIT - Link “https://startafacelesspage.com/?el=youtube”, EDIT - Calendly CTA “Want my direct help to build a $10k+?/mo Faceless Instagram Page; book a call here”, EDIT - Calendly Link “https://calendly.com/viralcreator/viral-creator-strategy-session-yt” (all Roboto 36, `#f2f2f2`) | The two link layers have an animator “Shared Link color” whose Fill Color = CTRL Link | static |
| **Cursor** | CURSOR - Figma PDF (24×24 PDF at 425 %, rotation −10°) | Drop Shadow 2 / 23.5 % / 18, Deep Glow radius 42, exposure 0.006 | Position 0.2667 s (1170, 3112.5) → 2.3333 s (534, 2108), out speed 0 @ 20 %, in speed 0 @ 88.08 %. No click. |

## 4. Knobs (template)
| # | Knob | Layer › path | Current value |
|---|---|---|---|
| 1 | Your video | YouTube Video comp (replace its 3 layers with footage) | placeholder “YOUR VIDEO · 16:9” |
| 2 | Video title | EDIT - Video title › `text/sourceText` | “Claude + Instagram = $32,561” |
| 3 | Channel name | EDIT - Channel › `text/sourceText` | “Tapa” |
| 4 | Subscribers | EDIT - Subscribers › `text/sourceText` | “17.7K subscribers” |
| 5 | Avatar image | YouTube Avatar › Tapa photo (footage) | Tapa.jpg |
| 6 | Likes | EDIT - Likes › `text/sourceText` | “39” |
| 7 | Views + date | EDIT - Views › `text/sourceText` | “4,334 views  Sep 28, 2026” |
| 8 | CTA line 1 | EDIT - CTA › `text/sourceText` | “Join my Live Free training on how build a Faceless Instagram Page:” |
| 9 | Link 1 (the cursor's target) | EDIT - Link › `text/sourceText` | “https://startafacelesspage.com/?el=youtube” |
| 10 | CTA line 2 | EDIT - Calendly CTA › `text/sourceText` | “Want my direct help …; book a call here” |
| 11 | Link 2 | EDIT - Calendly Link › `text/sourceText` | “https://calendly.com/viralcreator/viral-creator-strategy-session-yt” |
| 12 | Description box size / corners | Description - editable size and corners › `contents/group/contents/rect/size`, `…/roundness` | 3000×649, 34 |
| 13 | Description colour | CTRL - Global › `effects/#1/color` | `#373737` |
| 14 | Text colour | CTRL - Global › `effects/#2/color` | `#f2f2f2` |
| 15 | Link colour | CTRL - Global › `effects/#3/color` | `#3dadd1` (not visible today, see notes) |
| 16 | Page move timing | MOVE - YouTube page / MOVE - Page scale › key times (or the PAGE MOVE START/END markers) | 0.0667 → 2.2373 s |
| 17 | Page end framing | MOVE - YouTube page › `transform/position` key 2; MOVE - Page scale key 1 | y 760; start scale 86.1068 % |
| 18 | Cursor target and timing | CURSOR - Figma PDF › `transform/position` | (1170, 3112.5) @ 0.2667 → (534, 2108) @ 2.3333 |
| 19 | Cut back time | RETURN VIDEO › in-point; page + video layers' out-points | 2.6 s |
| 20 | Return defocus | RETURN VIDEO › `effects/#1/blurriness` | 28 → 0 over 0.2 s |

## 5. Distinctive parts
| Name | What it is | From | Call | Overlaps |
|---|---|---|---|---|
| `zoomOutToPage` | Full-frame clip hands off to a page that rises from below and scales 86 → 100 % (17.76 % out / 98.94 % in), the clip leaving through the top on one straight path tied to the page's progress | MOVE - YouTube page, MOVE - Page scale, VIDEO - replace in source comp | `zoomOutToPage(comp, {video, page, at, duration: 2.17, fromScale: 86.11, rise: 1067})` | none |
| `markerRetime` | Expression that plays a 2-key move between two named comp markers, so the timing is changed by dragging markers | MOVE nulls' position/scale expressions | `markerRetime(layer, path, {start: "PAGE MOVE START", end: "PAGE MOVE END"})` | none |
| `cursorClick` | Cursor glides from off-screen onto a target with a long settle (20 % out / 88 % in); here no press | CURSOR - Figma PDF | `cursorClick(comp, {to: [534, 2108], from: [1170, 3112.5], at: 0.2667, travel: 2.07, press: false})` | same id as proposals.json `cursorClick` |
| `defocusIn` | Cut back to a layer that racks from blur 28 to sharp in 0.2 s (20 % out / 70 % in), edge pixels repeated | RETURN VIDEO blur | `defocusIn(layer, {at, amount: 28, duration: 0.2})` | same id as dj3 `defocusIn` (there an adjustment layer, 40 in 0.3 s) |
| `youtubeWatchPage` | Editable YouTube watch-page details: title, round avatar, channel + subs, like/dislike and share pills, description box with views/date, CTA lines and links | YouTube Page + YouTube Avatar | `youtubeWatchPage(comp, {title, channel, subscribers, avatar, likes, views, lines: [...], links: [...]})` | none |
| `colorControlRig` | One CTRL null with Color controls that fills and text in other precomps read by expression: re-theme a template from one place | CTRL - Global + the `comp('YouTube Card')…` expressions | `colorControlRig(comp, {controls: {Description: "#373737", Text: "#f2f2f2", Link: "#3dadd1"}, targets})` | none (a STYLE-like idea inside a comp) |
| `videoPlaceholder` | Replaceable 16:9 video slot: dark plate, play icon, “YOUR VIDEO · 16:9” label, reused for leave and return | YouTube Video | `videoPlaceholder(comp, {label: "YOUR VIDEO · 16:9"})` | none |

## 6. Rebuild notes
- **Comp markers are not in the recipe.** The page and video expressions look for comp markers
  “PAGE MOVE START” / “PAGE MOVE END”; the rebuilt comp has none, so they error (“Marker … not
  found”) and the keyframes drive the layers. For the page nulls that is identical when the
  markers sit on the key times (0.0667 s and 2.2373 s); for the leaving video the expression would
  instead travel on one straight comp-space line over the whole page move. The rebuild still
  matches the source (PASS, inf dB), so the source renders the keyed version too. To bring the
  retiming back: `comp.addMarker {time: 0.0667, comment: "PAGE MOVE START"}` and `{time: 2.2373,
  comment: "PAGE MOVE END"}`, then check the video's exit.
- **Link colour does nothing visible**: the “Shared Link color” animators have no selector, and
  the links render in the Text colour (`#f2f2f2`).
- **Footage missing off Elias's Mac**: Play.pdf, Share.pdf, Cursor.pdf, ChannelAvatar.pdf
  (hidden) and Tapa.jpg live in `/Users/elias/Library/Caches/EffectCraft/Motion Library/blobs/…`.
  In a rebuild here the play icon, share icon, avatar and cursor don't show.
- **Deep Glow 2** (third-party, kept as raw PEDG params) on cursor, channel and title: radius 42,
  exposure 0.006, nearly invisible; check it after a rebuild if glows look off.
- Fonts: Roboto (Regular, SemiBold); the layout doesn't adapt if text widths change (pills and
  links are placed by hand).
- No random seeds: exact rebuild.
