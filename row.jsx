// row.jsx (scene) — a row of orbs, alternating circle and rounded square, staggered in.
#include "style.jsx"
#include "lib/kit.jsx"
#include "lib/background.jsx"
#include "lib/orb.jsx"
#include "lib/pop.jsx"
#include "lib/stagger.jsx"

var COUNT = 5;
var comp = target("Main", 1920, 1080, 2);
if (comp.isNew) background(comp);
var size = 0.22 * unit(comp), gap = 0.06 * unit(comp);
var total = COUNT * size + (COUNT - 1) * gap;
var items = [];
for (var i = 0; i < COUNT; i++) {
  items.push(orb(comp, { shape: i % 2 ? "rounded" : "circle", size: size,
    x: (comp.w - total) / 2 + size / 2 + i * (size + gap), name: "Orb " + (i + 1) }));
}
stagger(items, { at: comp.t, order: "center-out" });
"row built: " + COUNT + " orbs";
