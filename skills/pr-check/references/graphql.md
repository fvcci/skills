# Review-thread GraphQL

## List unresolved threads

Paginated — `reviewThreads` caps at 100 per page.

```bash
gh api graphql -f query='
query($cursor: String) {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 100, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes { body path }
          }
        }
      }
    }
  }
}'
```

If `hasNextPage` is true, re-run with `-f cursor=<endCursor>` until it is false.

## Resolve a thread

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "THREAD_ID"}) {
    thread { isResolved }
  }
}'
```

Batch several in one call with aliases:

```bash
gh api graphql -f query='
mutation {
  t1: resolveReviewThread(input: {threadId: "ID_1"}) { thread { isResolved } }
  t2: resolveReviewThread(input: {threadId: "ID_2"}) { thread { isResolved } }
}'
```
