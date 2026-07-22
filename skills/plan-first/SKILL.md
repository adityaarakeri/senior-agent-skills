---
name: plan-first
description: Write and confirm a short implementation plan before starting any large or risky change. Use this for tasks that touch three or more files, alter public APIs, database schemas, auth, payments, build systems, or CI, for migrations and multi-step refactors, and whenever the honest estimate is "this will take many steps". Also trigger it when the user asks "how would you approach this", says "plan", or when the request is ambiguous enough that two reasonable engineers would build different things.
---

# Plan First

Agents rarely fail big tasks by writing bad lines. They fail by sprinting confidently in the wrong direction for twenty minutes. A plan converts one giant gamble into a series of small, checkable bets, and it gives the human a chance to redirect you while redirecting is still cheap.

## When to plan (and when not to)

Plan when the change is wide (3+ files), deep (schemas, auth, public contracts, money), irreversible (migrations, deletions), or ambiguous (multiple valid interpretations). Skip the plan for single-file fixes, typos, and tasks with an obvious in-repo precedent to copy. The planning tax should match the risk, and a plan for a two-line fix is theater.

## The plan format

Keep it under a page. Longer plans stop being read.

```
Goal: one sentence, in the user's terms.
Non-goals: what this deliberately does NOT do.
Approach: 2-5 sentences on the how, including the key design decision.
Files to touch: the expected list, best guess.
Steps: ordered, each independently verifiable.
Risks: what could break, and the rollback story.
Verification: how we will know it worked (tests, manual check, metric).
```

## The rules

1. If anything in the task is ambiguous or destructive, show the plan and get a yes before executing. If the task is clear and safe, state the plan briefly and proceed; do not hold obvious work hostage to ceremony.
2. Execute step by step, and verify each step before starting the next. A plan you do not follow step-wise is just a longer prompt.
3. When reality disagrees with the plan (an assumption was wrong, a file does not exist, an API works differently), update the plan visibly. If the change is material, stop and say so rather than silently improvising a new design mid-flight. Silent pivots are how "rename a field" becomes "rewrote the persistence layer".
4. Non-goals are the highest-value section. Most scope creep is an agent helpfully doing things nobody asked for. Write down what you will not do, then actually do not do it.

## Example

Task: "Add rate limiting to our public API."

```
Goal: Reject requests over 100/min per API key on /api/v1/* with HTTP 429.
Non-goals: No per-endpoint limits, no billing integration, no admin UI.
Approach: Token bucket in the existing Redis, applied in middleware, keyed
by API key. Follows the pattern of the existing auth middleware.
Files: middleware/ratelimit.py (new), app.py (register), tests/test_ratelimit.py,
config.py (limits), docs/api.md.
Steps: 1) failing test for 101st request  2) middleware with hardcoded limit
3) config-driven limit  4) 429 body matches error schema  5) docs.
Risks: Redis outage should fail OPEN (availability over strictness); verify.
Verification: new tests green, full suite green, manual curl loop shows 429.
```
