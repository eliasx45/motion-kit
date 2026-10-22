// rect(comp, {w, h, radius, x, y, name}) — a rectangle in the hero look (the orb's gradient,
// inner shadow and hairline), so circles and rectangles match. w and h are in px (default from
// STYLE); radius is the corner radius as a fraction of the shorter side: 0 = sharp, 0.5 = pill.
// Needs orb.jsx (heroLook).
function rect(comp, o) {
  o = o || {};
  var r = STYLE.rect;
  var w = o.w || r.w * unit(comp), h = o.h || r.h * unit(comp);
  var short = Math.min(w, h);
  var radius = o.radius !== undefined ? o.radius : r.radius;
  var l = newShape({ comp: comp.id, kind: "rounded", size: [w, h], roundness: radius * short,
    position: [o.x !== undefined ? o.x : comp.w / 2, o.y !== undefined ? o.y : comp.h / 2],
    name: o.name || "Rectangle", fillType: "radial",
    stroke: STYLE.stroke.color, strokeWidth: px(comp, STYLE.stroke.width) });
  heroLook(l, short, r.reach * Math.sqrt(w * w + h * h) / 2);   // shadow by the short side; gradient toward the corners
  return l;
}
