# Feature Envy

Work sits away from the thing it belongs to. It has two forms:

- **A method envies data.** It reads another object's fields more than its own.
- **A caller does the owner's setup.** It builds a module's client, fetches its
  URL, reads its settings or writes its config, then hands the result over.

One test covers both: if the other module's details changed, would this code
have to change too? If yes, the work belongs over there.

A method that envies data:

```ts
// SMELL: a function in the order module reads four of the customer's fields
function shippingLabel(customer: Customer) {
  return `${customer.name}\n${customer.street}\n${customer.postcode} ${customer.city}`
}

// GOOD: the method lives on the customer, and shippingLabel is gone
class Customer {
  addressLabel() {
    return `${this.name}\n${this.street}\n${this.postcode} ${this.city}`
  }
}
```

Delete the old function and have its callers use the new method. An old
function kept as a one-line wrapper is a Middle Man.

A caller that does the owner's setup:

```ts
// SMELL: the entry point checks the writer's URL and builds the writer's client
const url = secrets.databaseUrl
if (!url) throw new Error('Missing database URL')
const writer = new UsageWriter(createClient({ url }))

// GOOD: the writer owns its connection
const writer = new UsageWriter(secrets)

class UsageWriter {
  private readonly client: Client

  constructor(secrets: Secrets) {
    if (!secrets.databaseUrl) throw new Error('Missing database URL')
    this.client = createClient({ url: secrets.databaseUrl })
  }
}
```

In the smell version, a change to how the writer connects means editing the
entry point. In the good version it means editing the writer only.

Fix: move the work to its owner. Move the method onto the data it reads, or
the setup into the module it sets up.

Leave it when the caller builds something several modules share, such as one
client used by three writers. That thing is the caller's to build.

The fix can create two smells. Stop moving work in once the owner would start
changing for an unrelated reason: that is Divergent Change. And delete what the
move leaves behind: a function that only forwards to the owner is a Middle Man.
