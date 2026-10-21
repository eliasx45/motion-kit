# inbox — candidates for the kit

While you're on a deadline, don't stop to build primitives. When you make something in an edit
that you'd want again, drop it here in 30 seconds and keep editing:

```sh
effectcraft-cli exec comp.recipe --params '{"comp":"My Edit","layers":["Card 1","Card 2"],"path":"'$PWD'/inbox/2026-10-21-card-row.recipe.json"}' --bridge
```

plus one line in `inbox/NOTES.md`: what it is and what you liked ("card row, the 2 f cascade
feels right"). After the deadline, each candidate becomes a primitive: values into `style.jsx`,
structure into `lib/`, proven with `build.sh` against the original.
