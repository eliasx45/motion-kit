// orb(comp, {shape: "circle"|"rounded", size, x, y, name}) — the style's hero shape:
// radial gradient, inner shadow, hairline stroke. size is in px (default from STYLE).
function orb(comp, o) {
  o = o || {};
  var s = STYLE.orb;
  var size = o.size || s.size * unit(comp);
  var rounded = o.shape === "rounded";
  var p = { comp: comp.id, kind: rounded ? "rounded" : "ellipse", size: [size, size],
    position: [o.x !== undefined ? o.x : comp.w / 2, o.y !== undefined ? o.y : comp.h / 2],
    name: o.name || (rounded ? "Rounded Square" : "Circle"), fillType: "radial",
    stroke: STYLE.stroke.color, strokeWidth: px(comp, STYLE.stroke.width) };
  if (rounded) p.roundness = s.roundness * size;
  var l = newShape(p);
  heroLook(l, size, size * (rounded ? 0.633 : 0.5));   // rounded: reach into the corners
  return l;
}

// heroLook(layer, size, reach) — the hero look on a new shape layer (orb, rect): the gradient
// runs from the centre out to `reach` px, and the inner shadow scales with `size` px.
function heroLook(l, size, reach) {
  var s = STYLE.orb, sh = STYLE.innerShadow;
  var g = "contents/group/contents/gfill/";
  set(l, g + "colors", { colors: [[0, s.inner], [s.midAt, s.mid], [1, s.outer]], opacities: [[0, 1], [1, 1]] });
  set(l, g + "start", [0, 0]);
  set(l, g + "end", [reach, 0]);

  app.run("layer.style.innerShadow", { layers: [l] });
  var st = "layerStyles/innerShadow/";
  set(l, st + "useGlobalLight", false);
  set(l, st + "angle", sh.angle);
  set(l, st + "distance", sh.distance * size);
  set(l, st + "size", sh.size * size);
  set(l, st + "choke", sh.choke);
  set(l, st + "opacity", sh.opacity);
  set(l, st + "color", sh.color);
}
