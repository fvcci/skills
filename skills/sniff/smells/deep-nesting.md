# Deep Nesting

Each block inside a block is one more condition the reader holds in their head
at once. It also spreads one rule over two places: a check sits at the top and
its `else` far below, so changing the rule means editing both.

Count depth by blocks. The function body is 1. Each `if`, `else`, loop,
`switch`, `try` or inline callback body inside it adds 1. Three deep is the
limit, and four deep is the smell. A named function starts a new count. Object
literals and markup are not blocks.

Two fixes, in this order:

1. **Inversion.** Flip the condition and return early. The unhappy path leaves
   first, and the `else` flattens into the main level. Repeated, it leaves a
   run of guard checks at the top that states what the function requires. The
   real work follows, unindented.
2. **Extraction.** Pull an inner block, such as a loop body or one branch,
   into its own function named for what it does. The outer function then reads
   as a list of its steps.

Inversion adds nothing new, so try it first. Extraction adds a function with
one user, so use it only when the code is still four deep.

Invert exactly: the opposite of `>` is `<=`, not `<`. The fix keeps behavior.

```ts
// SMELL: four deep
function registerUser(user: string) {
  const parts = user.split(':')
  if (parts.length === 2) {
    const userId = Number.parseInt(parts[0])
    if (userId >= 0) {
      const userName = parts[1]
      if (users.has(userId)) {
        users.get(userId).name = userName
      } else {
        users.set(userId, new User(userName))
      }
    } else {
      throw new Error(`Invalid user id: ${userId}`)
    }
  } else {
    throw new Error(`Invalid user string: ${user}`)
  }
}

// GOOD: two deep, guards first, then the work
function registerUser(user: string) {
  const parts = user.split(':')
  if (parts.length !== 2) {
    throw new Error(`Invalid user string: ${user}`)
  }

  const userId = Number.parseInt(parts[0])
  if (userId < 0) {
    throw new Error(`Invalid user id: ${userId}`)
  }

  const userName = parts[1]
  if (users.has(userId)) {
    users.get(userId).name = userName
  } else {
    users.set(userId, new User(userName))
  }
}
```

Extraction, when one long function does several jobs at depth. The real
`run()` below is about 100 lines. Each `// ...` stands for the lines cut here:

```ts
// SMELL: one function holds every job and every branch, seven deep
function run() {
  while (running) {
    // ... 10 lines: take new URLs off the request queue
    for (const download of downloads) {
      if (download.state === 'pending') {
        // ... 5 lines: start the download
      } else if (download.state === 'inProgress') {
        switch (download.process()) {
          case 'httpError':
            if (isRetriable(download)) {
              if (download.attempts > maxAttempts) {
                // ... 5 lines: move it to the failure queue
              }
            }
          // ... 25 lines: the other result codes, each with its own branches
        }
      }
    }
    // ... 15 lines: clear every download once the connection is disabled
    // ... 15 lines: wait for the next request
  }
}

// GOOD: each job has a name, and run() lists the steps
function run() {
  while (running) {
    processIncomingRequests()
    processDownloads()
    clearFinishedDownloads()
    waitForRequest()
  }
}
```

Source: CodeAesthetic, "Why You Shouldn't Nest Your Code",
<https://www.youtube.com/watch?v=CFRhGnuXG-4>. The limit of three is also in
the Linux kernel coding style: "if you need more than 3 levels of indentation,
you're screwed anyway, and should fix your program."
