# Module 2 — Reflection

**Team name**: _______________
**Branch**: `module-02/<team-name>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> *Your answer:*if you put everything in one file it works fine at first but 6 months later when someone new joins they open app.py and see SQL queries mixed with business logic mixed with HTTP responses and they have no idea where to even start looking. the layers help because if you need to swap SQLite for PostgreSQL, you only touch database.py and repository.py — routes.py and service.py dont need to change at all because they never talk to the database directly. same thing if the API shape changes, you only update schemas.py and routes.py and the rest of the code doesnt care. basically each layer protects you from having to change everything when one thing changes.

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.

> *Your answer:*game-service owns the games table. if activity-service could write to it directly, imagine this: activity-service has a bug and starts setting cover_url to null for every game it touches. now the games catalog is corrupted and game-service has no idea why because the writes are coming from somewhere else. it would be really hard to debug and game-service cant enforce its own rules about what valid game data looks like. when only game-service writes to its own table, if data is wrong you know exactly where to look.

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

> *Your answer:*for something this small with like 4 endpoints, having 5 separate files (models, schemas, repository, service, routes) feels like a lot of work for not much. in the monolith version of this we just wrote it all in app.py and it was done in like 30 minutes. the complexity starts paying off when the service grows — like when you add authentication, caching, or more complex business rules, having clean layers means you add that stuff in the right place without breaking what already works. for a tiny CRUD service the structure feels heavy, but the moment it needs to do more than basic CRUD it starts making sense.

---

*Keep this file. You will refer back to it during the oral presentation.*
