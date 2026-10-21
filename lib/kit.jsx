// kit.jsx — tiny helpers on top of app.run (which calls EffectCraft engine
// commands with JSON params: the "JSON inside JSX" pattern).
function unit(comp) { return Math.min(comp.w, comp.h); }          // the comp's shorter side
function px(comp, v) { return v * unit(comp) / 1080; }            // px at 1080p → px here
function set(layer, path, value) {
  return app.run("prop.set", { layer: layer, path: path, value: value });
}
function key(layer, path, time, value) {                          // adds a keyframe
  return app.run("prop.addKey", { layer: layer, path: path, time: time, value: value });
}
function ease(layer, keys) {                                      // keys: [{path, time}]
  var sel = [];
  for (var i = 0; i < keys.length; i++) sel.push({ layer: layer, path: keys[i].path, time: keys[i].time });
  app.run("keys.select", { keys: sel });
  app.run("keys.easyEase", {});
}
function newComp(name, w, h, duration) {
  var r = app.run("comp.new", { name: name, width: w, height: h, duration: duration || 4, frameRate: 29.97 });
  return { id: r.comp, name: name, w: w, h: h };
}
function newShape(p) {                                            // a NEW shape layer, never added into the selected one
  app.run("layer.select", { layers: [] });
  return app.run("shape.newShape", p).layer;
}
