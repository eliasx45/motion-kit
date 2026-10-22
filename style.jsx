// style.jsx — YOUR look, in one place. Every primitive reads from here.
// Sizes are fractions (of the comp's shorter side, or of the shape) so the
// look holds at 1920x1080, 1080x1920 and 4K alike. Times are in seconds.
var STYLE = {
  bg: {
    center: "#4d4f56",       // radial background, middle
    edge:   "#121317",       // radial background, corners
    reach:  1100 / 1920           // gradient radius, fraction of comp width
  },
  orb: {
    inner: "#8bd2ff",        // gradient centre (22 Oct: 20 % toward `mid`, so it blends instead of popping)
    mid:   "#3a7bff",        // gradient middle (stop at `midAt`)
    outer: "#1a1f6b",        // gradient edge
    midAt: 0.55,             // where the centre has melted into `mid` (22 Oct: 0.45 → 0.55, a larger, softer centre)
    size:  600 / 1080,       // default diameter, fraction of the comp's shorter side
    roundness: 0.2           // rounded square corner radius, fraction of size
  },
  rect: {
    w: 720 / 1080,           // default width, fraction of the comp's shorter side
    h: 360 / 1080,           // default height
    radius: 0.2,             // corner radius, fraction of the shorter side (0 sharp, 0.5 pill)
    reach: 0.895             // gradient radius, fraction of the half-diagonal (the rounded square's 0.633 × size)
  },
  stroke: { color: "#ffffff", width: 0.7 },          // px at 1080p, scaled with the comp
  innerShadow: {
    color: [0.03, 0.04, 0.2, 1],
    opacity: 70,
    angle: -60,              // degrees: shadow sits bottom-right
    distance: 36 / 600,         // fraction of shape size
    size: 70 / 600,            // softness, fraction of shape size
    choke: 10
  },
  stagger: {
    step: 0.08,              // seconds between one item's entrance and the next
    order: "in-order"        // in-order | reverse | center-out
  },
  slide: {
    distance: 120 / 1080,    // how far below it starts, fraction of the comp's shorter side
    duration: 1.0,           // seconds for one item's move
    outInfluence: 0,         // expo out: leaves its start at full speed…
    inInfluence: 100,        // …and glides into place
    fadeIn: 0.12             // seconds; hides the item until its move starts
  },
  pop: {
    overshoot: 115, undershoot: 95,   // scale %, the spring
    peakAt: 0.28, dipAt: 0.42, settleAt: 0.54, fadeIn: 0.12   // seconds
  }
};
