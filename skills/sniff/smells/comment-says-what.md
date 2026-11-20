# Comment Says What

Default to no comment. A comment earns its place only when its lines look
wrong, incomplete or arbitrary without it, and it gives the fact about other
code, or the outside constraint, that makes them right: a case left unhandled
because another module rules it out; a bug it works around; a caller's
requirement. Key on the lines, not the comment: if they would not tempt a
reader to change them, the comment goes, however true or hard-won its facts.

Delete on sight:
- Comments that restate the line below them.
- Comments that say what a declaration, value or case is, holds, means or is
  for: a class, field, interface, constant or function glossed in prose; what
  a set contains; what None, null or an empty value stands for; where a value
  comes from. They stay a smell when the fact lives elsewhere in the code, in
  the producer or a consumer: a reader changing the value reads those, and the
  comment goes stale when they change.
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

Before keeping a comment, point at the lines it sits on and say how they look
wrong or arbitrary without it. "A reader could misread what this holds" does
not count: that is a gloss. If you can't say it, delete the comment.
