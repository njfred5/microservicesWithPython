# Module 3 — Reflection

**Team name**: _______________
**Branch**: `module-03/<team-name>`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:*
honestly the thing that surprised me the most was how fragile it feels when one service needs to call another one. like when i was testing activity-service and forgot to start user-service first, everything just crashed. it made me realize that in a microservices setup you always have to think about what happens when the thing you depend on isnt there, which is something you never had to think about in the monolith because everything was in the same process.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> *Your answer:*
the user validation has to block the request because theres no point saving an activity for a user that doesnt exist, that would just be bad data. but the game enrichment is just extra info we attach to make the response nicer,the activity itself is still valid without it. so if game-service is down we just return null for the game field and the activity still gets saved. treating them differently means a game-service outage doesnt stop users from logging activities.
---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:*
every request now has to make an extra network hop through the gateway before it gets to the actual service. so if the gateway is slow or down, everything is slow or down even if all the services are fine. in the monolith there was no extra hop. but the trade-off is worth it because now clients only need to know one address and the gateway handles figuring out where to send things, and later it can also do auth checks in one place instead of every service doing it separately.
---

*Keep this file. You will refer back to it during the oral presentation.*
