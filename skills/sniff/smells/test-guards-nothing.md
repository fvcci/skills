# Test Guards Nothing

Keep a test only when it depends on the intended behavior: it changes only
when that behavior changes, and fails only when it regresses. A test that
guards nothing depends on something else. It has three forms:

- **It guards removed code.** A feature was removed and the test asserts it is
  gone, or a module moved and the test asserts it is absent from its old path.
  Removed code never changes, so the test can never catch a regression.
- **No change to the code can fail it.** It mocks the unit under test and
  asserts what the mock returns. It asserts what the type system already
  guarantees. It tests the platform: a `<button>` renders, or a click event
  fires.
- **Its expected value repeats the code's logic.** When the logic is wrong, the
  test is wrong the same way and still passes.

```ts
// SMELL: guards code that no longer exists
test('legacy exporter is gone', () => {
  expect(existsSync('src/export/legacy.ts')).toBe(false)
})

// SMELL: mocks the unit under test, then asserts the mock
test('loads the user', async () => {
  vi.spyOn(users, 'load').mockResolvedValue(alice)
  expect(await users.load(1)).toBe(alice)
})

// SMELL: the expected value repeats the code's logic
test('applies the discount', () => {
  const price = 100
  expect(applyDiscount(price, 0.2)).toBe(price - price * 0.2)
})

// GOOD: the expected value is written out
test('applies the discount', () => {
  expect(applyDiscount(100, 0.2)).toBe(80)
})
```

Fix: delete the test. Where it also covers behavior something relies on,
rewrite it against that behavior, as the discount test above was.
