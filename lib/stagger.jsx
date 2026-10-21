// stagger(layers, {at?, step?, order?, enter?}) — enter many layers one after another.
// `enter(layer, {at})` is the entrance (default pop), so any entrance primitive can be staggered.
// order: "in-order" (first to last), "reverse", "center-out" (middle first, spreading outwards).
function stagger(layers, o) {
  o = o || {};
  var at = o.at || 0, step = o.step !== undefined ? o.step : STYLE.stagger.step;
  var order = o.order || STYLE.stagger.order, enter = o.enter || pop;
  var n = layers.length, mid = (n - 1) / 2;
  for (var i = 0; i < n; i++) {
    var slot = order === "reverse" ? n - 1 - i
             : order === "center-out" ? Math.floor(Math.abs(i - mid))   // 5 items: 2,1,0,1,2
             : i;
    enter(layers[i], { at: at + slot * step });
  }
  return layers;
}
