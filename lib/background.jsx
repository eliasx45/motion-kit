// background(comp) — full-frame radial grey, sent to the back.
function background(comp, o) {
  o = o || {};
  var s = STYLE.bg;
  var l = newShape({ comp: comp.id, kind: "rect", size: [comp.w, comp.h],
    position: [comp.w / 2, comp.h / 2], name: o.name || "BG", fillType: "radial", strokeWidth: 0 });
  var g = "contents/group/contents/gfill/";
  set(l, g + "colors", { colors: [[0, o.center || s.center], [1, o.edge || s.edge]], opacities: [[0, 1], [1, 1]] });
  set(l, g + "start", [0, 0]);
  set(l, g + "end", [comp.w * s.reach, 0]);
  app.run("layer.arrange", { layers: [l], to: "back" });
  return l;
}
