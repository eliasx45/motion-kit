// hero.jsx (scene) — orb and rounded square on the radial background.
// Landscape: side by side. Portrait: stacked. Change W/H to re-target.
#include "style.jsx"
#include "lib/kit.jsx"
#include "lib/background.jsx"
#include "lib/orb.jsx"
#include "lib/pop.jsx"

var W = 1920, H = 1080;
if (typeof SIZE !== "undefined") { W = SIZE[0]; H = SIZE[1]; }   // set SIZE before including to override

var comp = target("Main", W, H, 2);
if (comp.isNew) background(comp);
var gap = 100 / 1080 * unit(comp);                 // 100 px at 1080p
var size = STYLE.orb.size * unit(comp);
var off = (size + gap) / 2;
var tall = comp.h > comp.w;
var a = tall ? { x: comp.w / 2, y: comp.h / 2 - off } : { x: comp.w / 2 - off, y: comp.h / 2 };
var b = tall ? { x: comp.w / 2, y: comp.h / 2 + off } : { x: comp.w / 2 + off, y: comp.h / 2 };
pop(orb(comp, { shape: "circle",  x: a.x, y: a.y }), { at: comp.t });
pop(orb(comp, { shape: "rounded", x: b.x, y: b.y }), { at: comp.t });
"hero built " + W + "x" + H;
