# Module 6 — Reflection

**Team name**: _______________
**Branch**: `module-06/<team-name>`
**Submitted**: before Module 7 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The gateway now validates every JWT before forwarding a request. Individual services no longer need to check identity themselves.

**What does centralising authentication at the gateway buy you?** What would the alternative look like — if every service validated tokens on its own?

Think about what happens when you need to rotate the secret key, or add a new service to the system.

> *Your answer:*

---centralizing auth at the gateway means every other service doesnt need to write the same token-checking code over and over. it also means theres only ONE place that decides if a request is allowed in or not, which is way easier to manage and update.

if every service checked tokens on its own, you would have the same validation logic copy pasted into 5+ different services, and if you ever need to change how validation works you'd have to update all of them and hope you didnt miss one. rotating the secret key would also be way harder, you'd need to update it everywhere at once instead of just in one place (gateway + auth-service). adding a new service would also be more work because that new service would also need its own copy of the validation logic instead of just trusting the gateway already checked it.

## 2. Your choice

When activity-service calls user-service internally, it uses a Machine-to-Machine (M2M) token — not a user's token.

**Why can't it just reuse the user's token that arrived in the original request?**

What would break, or what door would you accidentally leave open, if services passed user tokens between themselves?

> *Your answer:*

---it cant reuse the user's token because that token was meant for THAT specific user with THAT specific role, not for service-to-service communication. if activity-service passed the user's token along to user-service, user-service would think the USER themselves is making that request, which isnt true, its actually activity-service doing it on the user's behalf internally. also if we let services pass user tokens around, it would basically mean any service that touches a user token could pretend to be that user anywhere in the system. that's a security risk because it spreads the user's identity into places it was never meant to go. using a separate M2M token with its own role ("service") keeps things cleaner — its very clear in the logs and in the auth checks that this specific call came from a service, not a real user clicking something.


## 3. The tradeoff

The gateway and the auth-service share the same `SECRET_KEY` to verify tokens without making a network call on every request.

**What is the security risk of sharing this key?** What happens if it leaks?

And what would the alternative look like — verifying tokens by calling auth-service on every request instead? What does that cost you?

> *Your answer:*

---if the SECRET_KEY leaks, literally anyone who has it can create their own fake valid tokens and pretend to be any user or even an admin, since the gateway only checks the signature using that key, it has no way of knowing the token wasnt issued by the real auth-service. that would be a huge security hole, attacker could give themselves admin role in a fake token and the gateway would just accept it as real. The alternative is calling auth-service on every single request just to ask "is this token real?". that adds a network call AND extra latency to literally every request in the whole system, plus now auth-service becomes a single point that everything depends on, if it goes down even slightly slow, the entire system slows down or breaks with it. sharing the secret key avoids that cost but trades it for the risk of the key leaking, so its basically speed vs risk.

*Keep this file. You will refer back to it during the oral presentation.*
