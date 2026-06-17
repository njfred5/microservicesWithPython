# Module 5 — Reflection

**Team name**: _______________
**Branch**: `module-05/<team-name>`
**Submitted**: before Module 6 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The game-service now has two models for the same data: SQLite for writes, Redis for reads. They store the same games in two different shapes.

**Why go through the trouble of maintaining two representations of the same data?**

Think about what kind of queries each model is optimised for, and what would happen if you tried to use the write model for high-traffic read operations.

> *Your answer:*
the reason we keep two copies is because each one is good at a different job. SQLite is the "truth" copy, its slower but its always correct and complete. Redis is just a fast simple copy made for reading quick, like if 1000 people want to see a game summary at the same time, hitting SQLite that many times would be slow and could even lock up the database. Redis handles that kind of traffic way better because its built for fast reads. if we tried to use SQLite for all the high traffic reads it would probably get really slow and bottleneck the whole system, so splitting it into write model (SQLite) and read model (Redis) lets each one focus on what its actually good at.
---

## 2. Your choice

The logging-service checks GDPR consent before recording any activity. If a user has not opted in, the log is silently dropped.

**What does this consent check force you to accept about your data?** It is incomplete by design — some activities will never be recorded.

From a system design perspective: where is the right place to enforce this rule — in the logging-service, in the activity-service, or at the gateway? Why?

> *Your answer:*
this consent check basically means our data is never going to be 100% complete on purpose, because if someone doesnt opt in we are NOT allowed to log their activity at all, no matter what. so the dataset is always missing the people who opted out, and thats expected behavior not a bug.

for where to put this check, i think logging-service is the right place and not the gateway or activity-service. the gateway is too early in the chain, it doesnt even know what kind of data is being recorded, it just routes requests. activity-service also shouldnt have to know about consent rules, its only job is to track activities. logging-service is literally the one writing the logs, so it makes the most sense for it to be the one checking if its allowed to write before it writes. its also easier to test and change consent rules in one place instead of spreading that logic across multiple services.
---

## 3. The tradeoff

With CQRS, your write model and read model can drift out of sync — a game is updated in SQLite but the Redis projection still shows the old data.

**In what scenario does this inconsistency matter to the user? In what scenario is it completely acceptable?**

Is there a class of applications where eventual consistency is never acceptable? What are they?

> *Your answer:*

---it matters to the user when they need to see up to date info right away, like if they just updated a game's price or title and immediately check the summary page expecting to see the new info but it still shows the old one. that could confuse them or even cause a real problem like still showing the old price. its completely fine when the data isnt something the user is actively watching change in real time, like a leaderboard or game stats that update every few seconds is not a big deal if its a tiny bit behind. for stuff like banking or any payment processing, eventual consistency is never acceptable, you cant show someone an old balance after they just made a transaction, that has to be instant and accurate every time.

*Keep this file. You will refer back to it during the oral presentation.*
