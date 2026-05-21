## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: **\*\***\_\_\_**\*\***
**Branch**: `module-01/<team-name>`
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> _Your answer:_ so basically the problem we had with the monolith is if one thing breaks everything breaks, like if you just wanna fix the genre of a game in the catalog you gotta restart the whole app and while its restarting users cant log in, activities stop, notifications stop, like everything goes down for one tiny change that had nothing to do with any of that. splitting it into services means when the game-service restarts, the user-service doesnt even notice, users can still log in fine. so for the developer its easier to change one thing without being scared it breaks something else, and for the user they dont get kicked out just because someone fixed a typo somewhere.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> _Your answer:_the line i think is clearest is between user-service and activity-service. user-service owns users, activity-service owns activities. if we merged them together then every time we want to change something about how activities work, we'd also be touching the user code, and one bug could mess up logins. also they scale differently — if the platform gets busy with activity tracking you want to scale just that part up, not the whole user management system. keeping them separate means each one can grow at its own speed without dragging the other one.

---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> _Your answer:_in the monolith, if nova logs an activity and you want to check her username, you just do a JOIN — one database query, done. now with microservices, activity-service doesnt have direct access to the users table, so it has to make a network call to user-service to get the username. that adds latency, and if user-service is down for any reason, the activity request could fail too. so we traded "easy data access" for "independent deployments" which is a good trade overall but its definitely more complicated to deal with.

---

_Keep this file. You will refer back to it during the oral presentation._
