// shapes.jsx (scene) — the kit's basic shapes in one comp: circle and rounded square (orb) on
// top with a card (rect), then rectangles below: pill, chip, strip and a rounder strip. They pop
// in left to right, top row first. Landscape only.
#include "style.jsx"
#include "lib/kit.jsx"
#include "lib/background.jsx"
#include "lib/orb.jsx"
#include "lib/rect.jsx"
#include "lib/pop.jsx"
#include "lib/stagger.jsx"

var comp = target("Main", 1920, 1080, 2);
if (comp.isNew) background(comp);
var u = unit(comp) / 1080;                          // 1 px at 1080p
var cx = comp.w / 2, gap = 90 * u;

// Top row: circle 360, rounded square 360, card 720 × 360, centred as one row.
var top = comp.h / 2 - 210 * u, d = 360 * u, cardW = 720 * u;
var x0 = cx - (d + d + cardW + 2 * gap) / 2;
var row1 = [
  orb(comp, { shape: "circle", size: d, x: x0 + d / 2, y: top }),
  orb(comp, { shape: "rounded", size: d, x: x0 + d + gap + d / 2, y: top }),
  rect(comp, { w: cardW, h: d, x: x0 + 2 * (d + gap) + cardW / 2, y: top, name: "Card" })
];

// Bottom rows, 140 tall: pill (fully round ends), chip (soft corners), strip (nearly sharp),
// and under the strip the same strip a little rounder.
var low = comp.h / 2 + 160 * u, rh = 140 * u, w1 = 520 * u, w2 = 320 * u, w3 = 600 * u;
var x1 = cx - (w1 + w2 + w3 + 2 * gap) / 2, x3 = x1 + w1 + w2 + 2 * gap + w3 / 2;
var row2 = [
  rect(comp, { w: w1, h: rh, radius: 0.5, x: x1 + w1 / 2, y: low, name: "Pill" }),
  rect(comp, { w: w2, h: rh, radius: 0.3, x: x1 + w1 + gap + w2 / 2, y: low, name: "Chip" }),
  rect(comp, { w: w3, h: rh, radius: 0.08, x: x3, y: low, name: "Strip" }),
  rect(comp, { w: w3, h: rh, radius: 0.2, x: x3, y: low + rh + 50 * u, name: "Strip Rounded" })
];

stagger(row1.concat(row2), { at: comp.t, order: "in-order" });
"shapes built " + comp.w + "x" + comp.h;
