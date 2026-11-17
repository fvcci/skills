# Comment Says What

A comment earns its place by carrying information the code cannot: a reason,
a constraint, a link, a rejected alternative, a bug it works around, a
non-obvious consequence.

Delete on sight:
- Comments that restate the line below them.
- Section banners (`// --- helpers ---`) and step narration (`// Step 3: ...`).
- Docstrings that repeat the signature in prose.
- Changelog comments (`// added retry`, `// was 5, now 10`) — git owns that.
- `// TODO` you invented yourself and don't intend to do.

```ts
// SMELL: says what the code says
// Loop through users and add active ones to the list
for (const user of users) if (user.active) active.push(user)

// GOOD: says what the code can't
// Trials count as active until the grace period ends — billing reconciles nightly.
for (const user of users) if (isActive(user)) active.push(user)
```

Keep comments that a reader would otherwise ask "why is it like this?" about.
If you can't articulate the why, there wasn't one — delete the comment.
