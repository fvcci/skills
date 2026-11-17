# Mysterious Name

A reader must be able to tell what a class, function, or variable is from its
name, without opening the body or tracing the assignment. If a name needs a
comment to explain it, the name is wrong — fix the name, drop the comment.

- No `data`, `info`, `result`, `input`, `output`, `temp`, `obj`, `val`, `x` for anything with meaning.
- No `handle*`, `process*`, `manage*`, `doWork` — say what happens:
  `retryFailedWebhooks`, `parsePriceRow`.
- No `*Params`, `*Input`, `*Output` on a type — a name says what the thing
  is, not which side of a call it sits on: `Invoice`, not `BillingInput`;
  `RetryPolicy`, not `RetryParams`.
- Booleans read as assertions: `isExpired`, `hasWriteAccess`, `shouldRetry`.
- Units and currency belong in the name: `timeoutMs`, `priceUsdCents`.
- Names claim exactly what the code does. A `validateX` that also writes to
  the DB is a lie — rename it or split it.
- Short loop indices and `i`/`j` in tight scopes are fine. Scope length is the
  budget: the further a name travels, the more it has to say.

If a function needs a comment to describe what it does, either the name is too
vague or the function does too many things.
